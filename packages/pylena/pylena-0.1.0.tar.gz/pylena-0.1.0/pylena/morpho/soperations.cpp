#include <pln/core/image_cast.hpp>

#include <mln/morpho/closing.hpp>
#include <mln/morpho/dilation.hpp>
#include <mln/morpho/gradient.hpp>
#include <mln/morpho/opening.hpp>

#include "soperations.hpp"

namespace
{
  template <typename SE>
  struct erosion_t
  {
    mln::image2d<std::uint8_t> operator()(mln::image2d<std::uint8_t> img, const SE& se)
    {
      return mln::morpho::erosion(img, se);
    }
  };

  template <typename SE>
  struct dilation_t
  {
    mln::image2d<std::uint8_t> operator()(mln::image2d<std::uint8_t> img, const SE& se)
    {
      return mln::morpho::dilation(img, se);
    }
  };

  template <typename SE>
  struct opening_t
  {
    mln::image2d<std::uint8_t> operator()(mln::image2d<std::uint8_t> img, const SE& se)
    {
      return mln::morpho::opening(img, se);
    }
  };

  template <typename SE>
  struct closing_t
  {
    mln::image2d<std::uint8_t> operator()(mln::image2d<std::uint8_t> img, const SE& se)
    {
      return mln::morpho::closing(img, se);
    }
  };

  template <typename SE>
  struct gradient_t
  {
    mln::image2d<std::uint8_t> operator()(mln::image2d<std::uint8_t> img, const SE& se)
    {
      return mln::morpho::gradient(img, se);
    }
  };
} // namespace

namespace pln::morpho
{
  namespace details
  {
    template <template <typename> typename F, typename SE, typename... SEs>
    mln::ndbuffer_image morphological_operation_2d(mln::ndbuffer_image img, const structuring_element_2d& se)
    {
      if (se.type() == se2d_static_to_dyn<SE>::kind)
        return F<SE>()(*(img.cast_to<std::uint8_t, 2>()), se.as<SE>());
      else
      {
        if constexpr (!sizeof...(SEs))
          throw std::invalid_argument("Invalid structuring element");
        else
          return morphological_operation_2d<F, SEs...>(img, se);
      }
    }
  } // namespace details

  void def_operations(pybind11::module& m)
  {
    m.def("erosion", &details::morphological_operation_2d<erosion_t, mln::se::disc, mln::se::rect2d,
                                                          mln::se::periodic_line2d, details::mask2d>);
    m.def("dilation", &details::morphological_operation_2d<dilation_t, mln::se::disc, mln::se::rect2d,
                                                           mln::se::periodic_line2d, details::mask2d>);
    m.def("opening", &details::morphological_operation_2d<opening_t, mln::se::disc, mln::se::rect2d,
                                                          mln::se::periodic_line2d, details::mask2d>);
    m.def("closing", &details::morphological_operation_2d<closing_t, mln::se::disc, mln::se::rect2d,
                                                          mln::se::periodic_line2d, details::mask2d>);
    m.def("gradient", &details::morphological_operation_2d<gradient_t, mln::se::disc, mln::se::rect2d,
                                                           mln::se::periodic_line2d, details::mask2d>);
  }
} // namespace pln::morpho