pybind11_add_module(pylena_cxx module.cpp)
target_link_libraries(pylena_cxx PRIVATE Pylene::Pylene-numpy)

add_subdirectory(morpho)