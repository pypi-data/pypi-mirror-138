import numpy as np
import xobjects as xo

from ._pyparticles import Pyparticles

from ..general import _pkg_root

from scipy.constants import m_p
from scipy.constants import e as qe
from scipy.constants import c as clight

from xobjects import BypassLinked

pmass = m_p * clight * clight / qe

LAST_INVALID_STATE = -999999999

size_vars = (
    (xo.Int64,   '_capacity'),
    (xo.Int64,   '_num_active_particles'),
    (xo.Int64,   '_num_lost_particles'),
    )
# Capacity is always kept up to date
# the other two are placeholders to be used if needed
# i.e. on ContextCpu

scalar_vars = (
    (xo.Float64, 'q0'),
    (xo.Float64, 'mass0'),
    )

part_energy_vars = (
    (xo.Float64, 'psigma'),
    (xo.Float64, 'delta'),
    (xo.Float64, 'rpp'),
    (xo.Float64, 'rvv'),
        )

per_particle_vars = (
    (
        (xo.Float64, 'p0c'),
        (xo.Float64, 'gamma0'),
        (xo.Float64, 'beta0'),
        (xo.Float64, 's'),
        (xo.Float64, 'x'),
        (xo.Float64, 'y'),
        (xo.Float64, 'px'),
        (xo.Float64, 'py'),
        (xo.Float64, 'zeta'),
    )
    + part_energy_vars +
    (
        (xo.Float64, 'chi'),
        (xo.Float64, 'charge_ratio'),
        (xo.Float64, 'weight'),
        (xo.Int64, 'particle_id'),
        (xo.Int64, 'at_element'),
        (xo.Int64, 'at_turn'),
        (xo.Int64, 'state'),
        (xo.Int64, 'parent_particle_id'),
        (xo.UInt32, '__rng_s1'),
        (xo.UInt32, '__rng_s2'),
        (xo.UInt32, '__rng_s3'),
        (xo.UInt32, '__rng_s4')
    )
    )


fields = {}
for tt, nn in size_vars + scalar_vars:
    fields[nn] = tt

for tt, nn in per_particle_vars:
    fields[nn] = tt[:]

ParticlesData = type(
        'ParticlesData',
        (xo.Struct,),
        fields)

ParticlesData.extra_sources = [
    _pkg_root.joinpath('random_number_generator/rng_src/base_rng.h'),
    _pkg_root.joinpath('random_number_generator/rng_src/particles_rng.h')]
ParticlesData.custom_kernels = {
    'Particles_initialize_rand_gen': xo.Kernel(
        args=[
            xo.Arg(ParticlesData, name='particles'),
            xo.Arg(xo.UInt32, pointer=True, name='seeds'),
            xo.Arg(xo.Int32, name='n_init')],
        n_threads='n_init')}



class Particles(xo.dress(ParticlesData, rename={
                             'delta': '_delta',
                             'psigma': '_psigma',
                             'rvv': '_rvv',
                             'rpp': '_rpp'})):

    """
        Particle objects have the following fields:

             - s [m]:  Reference accumulated pathlength
             - x [m]:  Horizontal position
             - px[1]:  Px / (m/m0 * p0c) = beta_x gamma /(beta0 gamma0)
             - y [m]:  Vertical position
             - py [1]:  Py / (m/m0 * p0c)
             - delta[1]:  Pc / (m/m0 * p0c) - 1
             - ptau [1]:  Energy / (m/m0 * p0c) - 1
             - psigma [1]:  ptau/beta0
             - rvv [1]:  beta/beta0
             - rpp [1]:  1/(1+delta) = (m/m0 * p0c) / Pc
             - zeta [m]:  beta (s/beta0 - ct )
             - tau [m]:
             - sigma [m]:  s - beta0 ct = rvv * zeta
             - mass0 [eV]:
             - q0 [e]:  Reference charge
             - p0c [eV]: Reference momentum
             - energy0 [eV]: Reference energy
             - gamma0 [1]:  Reference relativistic gamma
             - beta0 [1]:  Reference relativistix beta
             - chi [1]:  q/ q0 * m0/m = qratio / mratio
             - mass_ratio [1]:  mass/mass0
             - charge_ratio [1]:  q / q0
             - particle_id [int]: Identifier of the particle
             - at_turn [int]:  Number of tracked turns
             - state [int]:  It is ``0`` if the particle is lost, ``1`` otherwise
             - weight [int]:  Particle weight in number of particles
                              (for collective sims.)
             - at_element [int]: Identifier of the last element through which
                                 the particle has been
             - parent_particle_id [int]: Identifier of the parent particle
                                         (secondary production processes)
    """

    _structure = {
            'size_vars': size_vars,
            'scalar_vars': scalar_vars,
            'per_particle_vars': per_particle_vars}

    def __init__(self, **kwargs):

        input_kwargs = kwargs.copy()

        if '_xobject' in kwargs.keys():
            # Initialize xobject
            self.xoinitialize(**kwargs)
        else:
            if any([nn in kwargs.keys() for tt, nn in per_particle_vars]):
                # Needed to generate consistent longitudinal variables
                pyparticles = Pyparticles(**kwargs)

                part_dict = _pyparticles_to_xpart_dict(pyparticles)
                if ('_capacity' in kwargs.keys() and
                         kwargs['_capacity'] is not None):
                    assert kwargs['_capacity'] >= part_dict['_num_particles']
                else:
                    kwargs['_capacity'] = part_dict['_num_particles']
            else:
                pyparticles = None
                if '_capacity' not in kwargs.keys():
                    kwargs['_capacity'] = 1

            # Make sure _capacity is integer
            kwargs['_capacity'] = int(kwargs['_capacity'])

            # We just provide array sizes to xoinitialize (we will set values later)
            kwargs.update(
                    {kk: kwargs['_capacity'] for tt, kk in per_particle_vars})

            # Initialize xobject
            self.xoinitialize(**kwargs)

            # Initialize coordinates
            with self._bypass_linked_vars():
                if pyparticles is not None:
                    context = self._buffer.context
                    for tt, kk in list(scalar_vars):
                        setattr(self, kk, part_dict[kk])
                    for tt, kk in list(per_particle_vars):
                        if kk.startswith('__'):
                            continue
                        vv = getattr(self, kk)
                        vals =  context.nparray_to_context_array(part_dict[kk])
                        ll = len(vals)
                        vv[:ll] = vals
                        vv[ll:] = LAST_INVALID_STATE
                else:
                    for tt, kk in list(scalar_vars):
                        setattr(self, kk, 0.)

                    for tt, kk in list(per_particle_vars):
                        if kk == 'chi' or kk == 'charge_ratio' or kk == 'state':
                            value = 1.
                        elif kk == 'particle_id':
                            value = np.arange(0, self._capacity, dtype=np.int64)
                        else:
                            value = 0.
                        getattr(self, kk)[:] = value

        self._num_active_particles = -1 # To be filled in only on CPU
        self._num_lost_particles = -1 # To be filled in only on CPU

        # Force values provided by user if compatible
        for nn in part_energy_varnames():
            vvv = self._buffer.context.nparray_from_context_array(getattr(self, nn))
            if nn in input_kwargs.keys():
                if hasattr(input_kwargs[nn], '__len__'):
                    ll = len(input_kwargs[nn]) # in case there is unallocated space
                else:
                    ll = len(vvv)

                if np.isscalar(input_kwargs[nn]):
                    getattr(self, "_"+nn)[:] = input_kwargs[nn]
                else:
                    getattr(self, "_"+nn)[:ll] = (
                            context.nparray_to_context_array(
                                np.array(input_kwargs[nn])))

        if isinstance(self._buffer.context, xo.ContextCpu):
            # Particles always need to be organized to run on CPU
            if '_no_reorganize' in kwargs.keys() and kwargs['_no_reorganize']:
                pass
            else:
                self.reorganize()

    def to_dict(self, copy_to_cpu=True,
                remove_underscored=None,
                remove_unused_space=None,
                remove_redundant_variables=None,
                keep_rng_state=None,
                compact=False):

        if remove_underscored is None:
            remove_underscored = True

        if remove_unused_space is None:
            remove_unused_space = compact

        if remove_redundant_variables is None:
            remove_redundant_variables = compact

        if keep_rng_state is None:
            keep_rng_state = not(compact)

        p_for_dict = self

        if copy_to_cpu:
            p_for_dict = p_for_dict.copy(_context=xo.context_default)

        if remove_unused_space:
            p_for_dict = p_for_dict.remove_unused_space()

        dct = super(p_for_dict.__class__, p_for_dict).to_dict()
        dct['delta'] = p_for_dict.delta
        dct['psigma'] = p_for_dict.psigma
        dct['rvv'] = p_for_dict.rvv
        dct['rpp'] = p_for_dict.rpp

        if remove_underscored:
            for kk in list(dct.keys()):
                if kk.startswith('_'):
                    if keep_rng_state and kk.startswith('__rng'):
                        continue
                    del(dct[kk])

        if remove_redundant_variables:
            for kk in ['psigma', 'rpp', 'rvv', 'gamma0', 'beta0']:
                del(dct[kk])

        return dct

    def to_pandas(self,
                  remove_underscored=None,
                  remove_unused_space=None,
                  remove_redundant_variables=None,
                  keep_rng_state=None,
                  compact=False):
        dct = self.to_dict(
                    remove_underscored=remove_underscored,
                    remove_unused_space=remove_unused_space,
                    remove_redundant_variables=remove_redundant_variables,
                    keep_rng_state=keep_rng_state,
                    compact=compact)
        import pandas as pd
        return pd.DataFrame(dct)

    @classmethod
    def from_pandas(cls, df, _context=None, _buffer=None, _offset=None):
        dct = df.to_dict(orient='list')
        for tt, nn in scalar_vars + size_vars:
            if nn in dct.keys() and not np.isscalar(dct[nn]):
                dct[nn] = dct[nn][0]
        return cls(**dct, _context=_context, _buffer=_buffer, _offset=_offset)

    @classmethod
    def merge(cls, lst, _context=None, _buffer=None, _offset=None):

        # TODO For now the merge is performed on CPU for add contexts.
        # Slow for objects on GPU (transferred to CPU for the merge).

        # Move everything to cpu
        cpu_lst = []
        for pp in lst:
            assert isinstance(pp, cls)
            if isinstance(pp._buffer.context, xo.ContextCpu):
                cpu_lst.append(pp)
            else:
                cpu_lst.append(pp.copy(_context=xo.context_default))

        # Check that scalar variable are compatible
        for tt, nn in scalar_vars:
            vals = [getattr(pp, nn) for pp in cpu_lst]
            assert np.allclose(vals,
                                getattr(cpu_lst[0], nn), rtol=0, atol=1e-14)

        # Make new particle on CPU
        capacity = np.sum([pp._capacity for pp in cpu_lst])
        new_part_cpu = cls(_capacity=capacity)

        # Copy scalar vars from first particle
        for tt, nn in scalar_vars:
            setattr(new_part_cpu, nn, getattr(cpu_lst[0], nn))

        # Copy per-particle vars
        first = 0
        max_id_curr = -1
        with new_part_cpu._bypass_linked_vars():
            for pp in cpu_lst:
                for tt, nn in per_particle_vars:
                    if not(nn == 'particle_id' or nn == 'parent_id'):
                        getattr(new_part_cpu, nn)[
                                first:first+pp._capacity] = getattr(pp, nn)

                # Handle particle_ids and parent_ids
                mask = pp.particle_id >= 0
                new_id = pp.particle_id.copy()
                new_parent_id = pp.parent_particle_id.copy()
                if np.min(new_id[mask]) <= max_id_curr:
                    new_id[mask] += (max_id_curr + 1)
                    new_parent_id[mask] += (max_id_curr + 1)
                new_part_cpu.particle_id[first:first+len(new_id)] = new_id
                new_part_cpu.parent_particle_id[
                        first:first+len(new_id)] = new_parent_id

                max_id_curr = np.max(new_id)
                first += pp._capacity

        # Reorganize
        new_part_cpu.reorganize()

        # Copy to appropriate context
        if _context is None and _buffer is None:
            # Use constext of first particle
            if isinstance(lst[0]._buffer.context, xo.ContextCpu):
                new_part_cpu._buffer.context = lst[0]._buffer.context
                return new_part_cpu
            else:
                return new_part_cpu.copy(_context=lst[0]._buffer.context)
        else:
            return new_part_cpu.copy(_context=_context, _buffer=_buffer,
                                     _offset=_offset)

    def filter(self, mask):

        if isinstance(self._buffer.context, xo.ContextCpu):
            self_cpu = self
        else:
            self_cpu = self.copy(_context=xo.context_default)

        # copy mask to cpu is needed
        if isinstance(mask, self._buffer.context.nplike_array_type):
            mask = self._buffer.context.nparray_from_context_array(mask)

            # Pyopencl returns int8 instead of bool
            if (isinstance(self._buffer.context, xo.ContextPyopencl) and
                mask.dtype==np.int8):
                assert np.all((mask>=0) & (mask<=1))
                mask = mask > 0

        # Make new particle on CPU
        test_x = self_cpu.x[mask]
        capacity = len(test_x)
        new_part_cpu = self.__class__(_capacity=capacity)

        # Copy scalar vars from first particle
        for tt, nn in scalar_vars:
            setattr(new_part_cpu, nn, getattr(self_cpu, nn))

        # Copy per-particle vars
        for tt, nn in per_particle_vars:
            with new_part_cpu._bypass_linked_vars():
                getattr(new_part_cpu, nn)[:] = getattr(self_cpu, nn)[mask]

        # Reorganize
        new_part_cpu.reorganize()

        # Copy to original context
        target_ctx = self._buffer.context
        if isinstance(target_ctx, xo.ContextCpu):
            new_part_cpu._buffer.context = target_ctx
            return new_part_cpu
        else:
            return new_part_cpu.copy(_context=target_ctx)

    def remove_unused_space(self):
        return self.filter(self.state > LAST_INVALID_STATE)

    def _bypass_linked_vars(self):
        return BypassLinked(self)

    def _init_random_number_generator(self, seeds=None):

         self.compile_custom_kernels(only_if_needed=True)

         if seeds is None:
            seeds = np.random.randint(low=1, high=4e9,
                        size=self._capacity, dtype=np.uint32)
         else:
            assert len(seeds) == particles._capacity
            if not hasattr(seeds, 'dtype') or seeds.dtype != np.uint32:
                seeds = np.array(seeds, dtype=np.uint32)

         context = self._buffer.context
         seeds_dev = context.nparray_to_context_array(seeds)
         context.kernels.Particles_initialize_rand_gen(particles=self,
             seeds=seeds_dev, n_init=self._capacity)

    def hide_lost_particles(self):
         self._lim_arrays_name = '_num_active_particles'
         self.reorganize()

    def unhide_lost_particles(self):
         del(self._lim_arrays_name)

    @property
    def lost_particles_are_hidden(self):
         return (hasattr(self, '_lim_arrays_name') and
                 self._lim_arrays_name == '_num_active_particles')

    def reorganize(self):
        assert not isinstance(self._buffer.context, xo.ContextPyopencl), (
                'Masking does not work with pyopencl')

        if self.lost_particles_are_hidden:
            restore_hidden = True
            self.unhide_lost_particles()
        else:
            restore_hidden = False

        mask_active = self.state > 0
        mask_lost = (self.state < 1) & (self.state>LAST_INVALID_STATE)

        n_active = np.sum(mask_active)
        n_lost = np.sum(mask_lost)

        with self._bypass_linked_vars():
            for tt, nn in self._structure['per_particle_vars']:
                vv = getattr(self, nn)
                vv_active = vv[mask_active]
                vv_lost = vv[mask_lost]

                vv[:n_active] = vv_active
                vv[n_active:n_active+n_lost] = vv_lost
                vv[n_active+n_lost:] = LAST_INVALID_STATE

        if isinstance(self._buffer.context, xo.ContextCpu):
            self._num_active_particles = n_active
            self._num_lost_particles = n_lost

        if restore_hidden:
            self.hide_lost_particles()

        return n_active, n_lost

    def add_particles(self, part, keep_lost=False):

        if keep_lost:
            raise NotImplementedError
        assert not isinstance(self._buffer.context, xo.ContextPyopencl), (
                'Masking does not work with pyopencl')

        mask_copy = part.state > 0
        n_copy = np.sum(mask_copy)

        n_active, n_lost = self.reorganize()
        i_start_copy = n_active + n_lost
        n_free = self._capacity - n_active - n_lost

        max_id = np.max(self.particle_id[:n_active+n_lost])

        if n_copy > n_free:
            raise NotImplementedError("Out of space, need to regenerate xobject")

        for tt, nn in self._structure['scalar_vars']:
            assert np.isclose(getattr(self, nn), getattr(part, nn),
                    rtol=1e-14, atol=1e-14)

        with self._bypass_linked_vars():
            for tt, nn in self._structure['per_particle_vars']:
                vv = getattr(self, nn)
                vv_copy = getattr(part, nn)[mask_copy]
                vv[i_start_copy:i_start_copy+n_copy] = vv_copy

        self.particle_id[i_start_copy:i_start_copy+n_copy] = np.arange(
                                     max_id+1, max_id+1+n_copy, dtype=np.int64)

        self.reorganize()

    def get_active_particle_id_range(self):
        ctx2np = self._buffer.context.nparray_from_context_array
        mask_active = ctx2np(self.state) > 0
        ids_active_particles = ctx2np(self.particle_id)[mask_active]
        # Behaves as python range (+1)
        return np.min(ids_active_particles), np.max(ids_active_particles)+1

    def _set_p0c(self):
        energy0 = np.sqrt(self.p0c ** 2 + self.mass0 ** 2)
        self.beta0 = self.p0c / energy0
        self.gamma0 = energy0 / self.mass0

    @property
    def delta(self):
        return self._buffer.context.linked_array_type.from_array(
                                        self._delta,
                                        mode='setitem_from_container',
                                        container=self,
                                        container_setitem_name='_delta_setitem')

    @delta.setter
    def delta(self, value):
        self.delta[:] = value

    def _delta_setitem(self, indx, val):
        self._delta[indx] = val
        self.update_delta(self._delta)

    @property
    def psigma(self):
        return self._buffer.context.linked_array_type.from_array(
                                            self._psigma, mode='readonly',
                                            container=self)

    @property
    def rvv(self):
        return self._buffer.context.linked_array_type.from_array(
                                            self._rvv, mode='readonly',
                                            container=self)

    @property
    def rpp(self):
        return self._buffer.context.linked_array_type.from_array(
                                            self._rpp, mode='readonly',
                                            container=self)

    @property
    def ptau(self):
        return (
            np.sqrt(self.delta ** 2 + 2 * self.delta + 1 / self.beta0 ** 2)
            - 1 / self.beta0
        )

    @property
    def energy0(self):
        return np.sqrt( self.p0c * self.p0c + self.mass0 * self.mass0 )

    @property
    def energy(self):
        return self.energy0 + self.psigma * self.p0c * self.beta0 # eV

    def add_to_energy(self, delta_energy):
        beta0 = self.beta0.copy()
        delta_beta0 = self.delta * beta0

        ptau_beta0 = (
            delta_energy / self.energy0.copy() +
            np.sqrt( delta_beta0 * delta_beta0 + 2.0 * delta_beta0 * beta0
                    + 1. ) - 1.)

        ptau   = ptau_beta0 / beta0
        psigma = ptau / beta0
        delta = np.sqrt( ptau * ptau + 2. * psigma + 1 ) - 1

        one_plus_delta = delta + 1.
        rvv = one_plus_delta / ( 1. + ptau_beta0 )

        self._delta = delta
        self._psigma = psigma
        self._zeta *= rvv / self.rvv

        self._rvv = rvv
        self._rpp = 1. / one_plus_delta

    def set_particle(self, index, set_scalar_vars=False,
            check_scalar_vars=True, **kwargs):

        # Needed to generate consistent longitudinal variables
        pyparticles = Pyparticles(**kwargs)
        part_dict = _pyparticles_to_xpart_dict(pyparticles)
        for tt, kk in list(scalar_vars):
            setattr(self, kk, part_dict[kk])
        for tt, kk in list(per_particle_vars):
            if kk.startswith('__') and kk not in part_dict.keys():
                continue
            getattr(self, kk)[index] = part_dict[kk][0]

    def update_delta(self, new_delta_value):
        beta0 = self.beta0
        delta_beta0 = new_delta_value * beta0
        ptau_beta0  = ( delta_beta0 * delta_beta0 +
                                2. * delta_beta0 * beta0 + 1. )**0.5 - 1.
        one_plus_delta = 1. + new_delta_value
        rvv    = ( one_plus_delta ) / ( 1. + ptau_beta0 )
        rpp    = 1. / one_plus_delta
        psigma = ptau_beta0 / ( beta0 * beta0 )

        self._delta[:] = new_delta_value
        self._rvv[:] = rvv
        self._rpp[:] = rpp
        self._psigma[:] = psigma

def _str_in_list(string, str_list):

    found = False
    for ss in str_list:
        # TODO: Tried this but did not work
        # To avoid strange behaviors with different str formats
        # if ss.decode('utf-8') == string.decode('utf-8'):
        if ss == string:
            found = True
            break
    return found

def part_energy_varnames():
    return [vv for tt, vv in part_energy_vars]

def gen_local_particle_api(mode='no_local_copy', freeze_vars=()):

    if mode != 'no_local_copy':
        raise NotImplementedError

    src_lines = []
    src_lines.append('''typedef struct{''')
    for tt, vv in size_vars + scalar_vars:
        src_lines.append('                 ' + tt._c_type + '  '+vv+';')
    for tt, vv in per_particle_vars:
        src_lines.append('    /*gpuglmem*/ ' + tt._c_type + '* '+vv+';')
    src_lines.append(    '                 int64_t ipart;')
    src_lines.append('}LocalParticle;')
    src_typedef = '\n'.join(src_lines)

    # Particles_to_LocalParticle
    src_lines = []
    src_lines.append('''
    /*gpufun*/
    void Particles_to_LocalParticle(ParticlesData source,
                                    LocalParticle* dest,
                                    int64_t id){''')
    for tt, vv in size_vars + scalar_vars:
        src_lines.append(
                f'  dest->{vv} = ParticlesData_get_'+vv+'(source);')
    for tt, vv in per_particle_vars:
        src_lines.append(
                f'  dest->{vv} = ParticlesData_getp1_'+vv+'(source, 0);')
    src_lines.append('  dest->ipart = id;')
    src_lines.append('}')
    src_particles_to_local = '\n'.join(src_lines)

    # LocalParticle_to_Particles
    src_lines = []
    src_lines.append('''
    /*gpufun*/
    void LocalParticle_to_Particles(
                                    LocalParticle* source,
                                    ParticlesData dest,
                                    int64_t id,
                                    int64_t set_scalar){''')
    src_lines.append('if (set_scalar){')
    for tt, vv in size_vars + scalar_vars:
        src_lines.append(
                f'  ParticlesData_set_' + vv + '(dest,'
                f'      LocalParticle_get_{vv}(source));')
    src_lines.append('}')

    for tt, vv in per_particle_vars:
        src_lines.append(
                f'  ParticlesData_set_' + vv + '(dest, id, '
                f'      LocalParticle_get_{vv}(source));')
    src_lines.append('}')
    src_local_to_particles = '\n'.join(src_lines)

    # Adders
    src_lines=[]
    for tt, vv in per_particle_vars:
        src_lines.append('''
    /*gpufun*/
    void LocalParticle_add_to_'''+vv+f'(LocalParticle* part, {tt._c_type} value)'
    +'{')
        if _str_in_list(vv, freeze_vars):
            src_lines.append('/* frozen variable!')
        src_lines.append(f'  part->{vv}[part->ipart] += value;')
        if _str_in_list(vv, freeze_vars):
            src_lines.append('frozen variable!*/')
        src_lines.append('}\n')
    src_adders = '\n'.join(src_lines)

    # Scalers
    src_lines=[]
    for tt, vv in per_particle_vars:
        src_lines.append('''
    /*gpufun*/
    void LocalParticle_scale_'''+vv+f'(LocalParticle* part, {tt._c_type} value)'
    +'{')
        if _str_in_list(vv, freeze_vars):
            src_lines.append('/* frozen variable!')
        src_lines.append(f'  part->{vv}[part->ipart] *= value;')
        if _str_in_list(vv, freeze_vars):
            src_lines.append('frozen variable!*/')
        src_lines.append('}\n')
    src_scalers = '\n'.join(src_lines)

    # Setters
    src_lines=[]
    for tt, vv in per_particle_vars:
        src_lines.append('''
    /*gpufun*/
    void LocalParticle_set_'''+vv+f'(LocalParticle* part, {tt._c_type} value)'
    +'{')
        if _str_in_list(vv, freeze_vars):
            src_lines.append('/* frozen variable!')
        src_lines.append(f'  part->{vv}[part->ipart] = value;')
        if _str_in_list(vv, freeze_vars):
            src_lines.append('frozen variable!*/')
        src_lines.append('}')
    src_setters = '\n'.join(src_lines)

    # Getters
    src_lines=[]
    for tt, vv in size_vars + scalar_vars:
        src_lines.append('/*gpufun*/')
        src_lines.append(f'{tt._c_type} LocalParticle_get_'+vv
                        + f'(LocalParticle* part)'
                        + '{')
        src_lines.append(f'  return part->{vv};')
        src_lines.append('}')
    for tt, vv in per_particle_vars:
        src_lines.append('/*gpufun*/')
        src_lines.append(f'{tt._c_type} LocalParticle_get_'+vv
                        + f'(LocalParticle* part)'
                        + '{')
        src_lines.append(f'  return part->{vv}[part->ipart];')
        src_lines.append('}')
    src_getters = '\n'.join(src_lines)

    # Particle exchangers
    src_exchange = '''
/*gpufun*/
void LocalParticle_exchange(LocalParticle* part, int64_t i1, int64_t i2){
'''
    for tt, vv in per_particle_vars:
        src_exchange += '\n'.join([
          '\n    {',
          f'    {tt._c_type} temp = part->{vv}[i2];',
          f'    part->{vv}[i2] = part->{vv}[i1];',
          f'    part->{vv}[i1] = temp;',
          '     }'])
    src_exchange += '}\n'


    custom_source='''
/*gpufun*/
double LocalParticle_get_energy0(LocalParticle* part){

    double const p0c = LocalParticle_get_p0c(part);
    double const m0  = LocalParticle_get_mass0(part);

    return sqrt( p0c * p0c + m0 * m0 );
}

/*gpufun*/
void LocalParticle_add_to_energy(LocalParticle* part, double delta_energy, int pz_only ){

    double const beta0 = LocalParticle_get_beta0(part);
    double const delta_beta0 = LocalParticle_get_delta(part) * beta0;

    double const ptau_beta0 =
        delta_energy / LocalParticle_get_energy0(part) +
        sqrt( delta_beta0 * delta_beta0 + 2.0 * delta_beta0 * beta0
                + 1. ) - 1.;

    double const ptau   = ptau_beta0 / beta0;
    double const psigma = ptau / beta0;
    double const delta = sqrt( ptau * ptau + 2. * psigma + 1 ) - 1;

    double const one_plus_delta = delta + 1.;
    double const rvv = one_plus_delta / ( 1. + ptau_beta0 );

    LocalParticle_set_delta(part, delta );
    LocalParticle_set_psigma(part, psigma );
    LocalParticle_scale_zeta(part,
        rvv / LocalParticle_get_rvv(part));

    LocalParticle_set_rvv(part, rvv );

    double const new_rpp = 1. / one_plus_delta;

    if (!pz_only) {
        double const old_rpp = LocalParticle_get_rpp(part);
        double const f = old_rpp / new_rpp;
        LocalParticle_scale_px(part, f);
        LocalParticle_scale_py(part, f);
    }

    LocalParticle_set_rpp(part, new_rpp );
}

/*gpufun*/
void LocalParticle_update_delta(LocalParticle* part, double new_delta_value){
    double const beta0 = LocalParticle_get_beta0(part);
    double const delta_beta0 = new_delta_value * beta0;
    double const ptau_beta0  = sqrt( delta_beta0 * delta_beta0 +
                                2. * delta_beta0 * beta0 + 1. ) - 1.;

    double const one_plus_delta = 1. + new_delta_value;
    double const rvv    = ( one_plus_delta ) / ( 1. + ptau_beta0 );
    double const rpp    = 1. / one_plus_delta;
    double const psigma = ptau_beta0 / ( beta0 * beta0 );

    LocalParticle_set_delta(part, new_delta_value);

    LocalParticle_set_rvv(part, rvv );
    LocalParticle_set_rpp(part, rpp );
    LocalParticle_set_psigma(part, psigma );

}

/*gpufun*/
void LocalParticle_update_p0c(LocalParticle* part, double new_p0c_value){

    double const mass0 = LocalParticle_get_mass0(part);
    double const old_p0c = LocalParticle_get_p0c(part);
    double const old_delta = LocalParticle_get_delta(part);

    double const ppc = old_p0c * old_delta + old_p0c;
    double const new_delta = (ppc - new_p0c_value)/new_p0c_value;

    double const new_energy0 = sqrt(new_p0c_value*new_p0c_value + mass0 * mass0);
    double const new_beta0 = new_p0c_value / new_energy0;
    double const new_gamma0 = new_energy0 / mass0;

    LocalParticle_set_p0c(part, new_p0c_value);
    LocalParticle_set_gamma0(part, new_gamma0);
    LocalParticle_set_beta0(part, new_beta0);

    LocalParticle_update_delta(part, new_delta);

    LocalParticle_scale_px(part, old_p0c/new_p0c_value);
    LocalParticle_scale_py(part, old_p0c/new_p0c_value);

}
'''

    source = '\n\n'.join([src_typedef, src_adders, src_getters,
                          src_setters, src_scalers, src_exchange,
                          src_particles_to_local, src_local_to_particles,
                          custom_source])

    return source

def _pyparticles_to_xpart_dict(pyparticles):

    out = {}

    dct = pyparticles.to_dict()

    if hasattr(pyparticles, 'weight'):
        dct['weight'] = getattr(pyparticles, 'weight')
    else:
        dct['weight'] = 1.

    for tt, kk in scalar_vars + per_particle_vars:
        if kk.startswith('__'):
            continue
        # Use properties
        dct[kk] = getattr(pyparticles, kk)


    for kk, vv in dct.items():
        dct[kk] = np.atleast_1d(vv)

    lll = [len(vv) for kk, vv in dct.items() if hasattr(vv, '__len__')]
    lll = list(set(lll))
    assert len(set(lll) - {1}) <= 1
    _num_particles = max(lll)
    out['_num_particles'] = _num_particles

    for tt, kk in scalar_vars:
        val = dct[kk]
        assert np.allclose(val, val[0], rtol=1e-10, atol=1e-14)
        out[kk] = val[0]

    for tt, kk in per_particle_vars:
        if kk.startswith('__'):
            continue

        val_py = dct[kk]

        if _num_particles > 1 and len(val_py)==1:
            temp = np.zeros(int(_num_particles), dtype=tt._dtype)
            temp += val_py[0]
            val_py = temp

        if type(val_py) != tt._dtype:
            val_py = np.array(val_py, dtype=tt._dtype)

        out[kk] = val_py

    #out['_num_active_particles'] = np.sum(out['state']>0)
    #out['_num_lost_particles'] = np.sum((out['state'] < 0) &
    #                                      (out['state'] > LAST_INVALID_STATE))

    return out
