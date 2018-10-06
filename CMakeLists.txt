cmake_minimum_required(VERSION 3.0.2)
project(Jinja2Cpp VERSION 0.9.0)

# Requirements
find_package(expected_lite REQUIRED)
find_package(variant_lite REQUIRED)
find_package(value_ptr_lite REQUIRED)
find_package(optional_lite REQUIRED)
find_package(Boost 1.65 REQUIRED COMPONENTS filesystem)


list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake)

set(JINJA2CPP_IS_MAIN_PROEJCT TRUE)
option(JINJA2CPP_BUILD_TESTS "Build Jinja2Cpp unit tests" ${JINJA2CPP_IS_MAIN_PROEJCT})

include(collect_sources)

set (LIB_TARGET_NAME jinja2cpp)

CollectSources(Sources Headers ${CMAKE_CURRENT_SOURCE_DIR} ${CMAKE_CURRENT_SOURCE_DIR}/src)
CollectSources(PublicSources PublicHeaders ${CMAKE_CURRENT_SOURCE_DIR} ${CMAKE_CURRENT_SOURCE_DIR}/include)

add_library(${LIB_TARGET_NAME} STATIC
    ${Sources}
    ${Headers}
    ${PublicHeaders}
    )

target_link_libraries(${LIB_TARGET_NAME} PUBLIC expected_lite variant_lite value_ptr_lite optional_lite Boost::boost Boost::filesystem Boost::disable_autolinking)

target_include_directories(${LIB_TARGET_NAME}
    PUBLIC "$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>" "$<INSTALL_INTERFACE:include>")


if(NOT MSVC)
    # Enable -Werror and -Wall on jinja2cpp target, ignoring warning errors from thirdparty libs
    include(CheckCXXCompilerFlag)
    check_cxx_compiler_flag(-Wno-error=parentheses COMPILER_HAS_WNO_ERROR_PARENTHESES_FLAG)
    check_cxx_compiler_flag(-Wno-error=deprecated-declarations COMPILER_HAS_WNO_ERROR_DEPRECATED_DECLARATIONS_FLAG)
    check_cxx_compiler_flag(-Wno-error=maybe-uninitialized COMPILER_HAS_WNO_ERROR_MAYBE_UNINITIALIZED_FLAG)

    if(COMPILER_HAS_WNO_ERROR_PARENTHESES_FLAG)
        target_compile_options(boost_assert INTERFACE -Wno-error=parentheses)
    endif()
    if(COMPILER_HAS_WNO_ERROR_DEPRECATED_DECLARATIONS_FLAG)
        target_compile_options(boost_filesystem PRIVATE -Wno-error=deprecated-declarations)
    endif()
    if(COMPILER_HAS_WNO_ERROR_MAYBE_UNINITIALIZED_FLAG)
        target_compile_options(boost_variant INTERFACE -Wno-error=maybe-uninitialized)
    endif()

    target_compile_options(${LIB_TARGET_NAME} PRIVATE -Wall -Werror)
endif()

if (JINJA2CPP_BUILD_TESTS)
    enable_testing()
    find_package(GTest REQUIRED)
    
    CollectSources(TestSources TestHeaders ${CMAKE_CURRENT_SOURCE_DIR} ${CMAKE_CURRENT_SOURCE_DIR}/test)
    add_executable(jinja2cpp_tests ${TestSources} ${TestHeaders})
    target_link_libraries(jinja2cpp_tests GTest::Main GTest::GTest ${LIB_TARGET_NAME})

    add_custom_command(
        OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/test_data/simple_template1.j2tpl
        COMMAND ${CMAKE_COMMAND} ARGS -E copy_directory ${CMAKE_CURRENT_SOURCE_DIR}/test/test_data ${CMAKE_CURRENT_BINARY_DIR}/test_data
        MAIN_DEPENDENCY ${CMAKE_CURRENT_SOURCE_DIR}/test/test_data/simple_template1.j2tpl
        COMMENT "Copy test data to the destination dir"
        )

    add_custom_target(CopyTestData ALL
        DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/test_data/simple_template1.j2tpl
        )

    add_test(NAME jinja2cpp_tests COMMAND jinja2cpp_tests)
endif ()

install(TARGETS ${LIB_TARGET_NAME}
        RUNTIME DESTINATION bin
        LIBRARY DESTINATION lib
        ARCHIVE DESTINATION lib/static)

install (DIRECTORY include/ DESTINATION include)

#
# Create Config Files
#
install(TARGETS ${LIB_TARGET_NAME}
    EXPORT Targets
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
    RUNTIME DESTINATION bin
    INCLUDES DESTINATION include
    )

install(EXPORT Targets
    FILE ${PROJECT_NAME}Targets.cmake
    DESTINATION share/cmake/${PROJECT_NAME}
    )

#
# Export Library
#
include(CMakePackageConfigHelpers)

write_basic_package_version_file("${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}ConfigVersion.cmake"
    VERSION ${PROJECT_VERSION}
    COMPATIBILITY SameMinorVersion
    )

configure_file(
    "${CMAKE_CURRENT_SOURCE_DIR}/cmake/public/LibraryConfig.cmake.in"
    "${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}Config.cmake"
    @ONLY
    )

install(
    FILES
        "${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}ConfigVersion.cmake"
        "${CMAKE_CURRENT_BINARY_DIR}/${PROJECT_NAME}Config.cmake"
    DESTINATION
        . # Root Directory
    )
