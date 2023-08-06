project(tquant_api)

include_directories(
  api
)

set(SRC
  api/tquant_api.h
  api/impl_tquant_api.h
  api/impl_tquant_api.cpp
  api/impl_data_api.h
  api/impl_trade_api.h
  api/tqapi_cs.cpp
  api/tqapi_cs.h
  api/tqapi_ffi.h
  api/tqapi_ffi_dapi.cpp
  api/tqapi_ffi_tapi.cpp
)

if (UNIX)
  set (DL_LIB dl)
endif()

# Static library
add_library(tqapi-static STATIC ${SRC})
target_link_libraries(tqapi-static
  jsoncpp
  myutils
  msgpack
  snappy
  ${DL_LIB}
  ${COMMON_LIB}
)

# Shared Library
add_library(tqapi SHARED ${SRC})
target_link_libraries(tqapi
  jsoncpp
  myutils
  msgpack
  snappy
  ${DL_LIB}
  ${COMMON_LIB}
)
target_compile_definitions(tqapi PRIVATE _TQAPI_DLL_IMPL=1)

install(TARGETS tqapi DESTINATION bin)
install(TARGETS tqapi-static DESTINATION cpp)

install(FILES
  api/tquant_api.h
  DESTINATION cpp
)

# Test

add_executable(tqapi_test
  api/tquant_api_test.cpp
)

target_link_libraries(tqapi_test tqapi-static)

install(TARGETS tqapi_test DESTINATION bin)