cmake_minimum_required (VERSION 3.8)
include(FetchContent)

project ("maimai")

# Add source to this project's executable.
add_executable (maimai-score-control "src/score_control.cc")

if (CMAKE_VERSION VERSION_GREATER 3.12)
  set_property(TARGET maimai-score-control PROPERTY CXX_STANDARD 20)
endif()

# Fetch csv-parser and make it available to my-executable
FetchContent_Declare(
  csv  
  GIT_REPOSITORY https://github.com/vincentlaucsb/csv-parser.git
  GIT_SHALLOW TRUE 
  GIT_TAG 2.3.0
) 

FetchContent_MakeAvailable(csv)

target_include_directories(maimai-score-control PRIVATE csv)
target_link_libraries(maimai-score-control csv)