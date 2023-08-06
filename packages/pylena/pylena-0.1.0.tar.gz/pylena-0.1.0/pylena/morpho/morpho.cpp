#include "morpho.hpp"

#include "se.hpp"
#include "soperations.hpp"

namespace pln::morpho
{
  void define_morpho(pybind11::module& _m)
  {
    auto m = _m.def_submodule("morpho");
    pln::morpho::def_se(m);
    pln::morpho::def_operations(m);
  }
} // namespace pln::morpho