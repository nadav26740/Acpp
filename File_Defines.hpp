#pragma once
#include <iostream>
#include <string>
#include <vector>

// paths defines
#define CUSTOM_COMPILER_CAECH_FOLDER (std::string)(".AutoCompiler")
#define CODES_FILES_LIST_FILE (std::string)(CUSTOM_COMPILER_CAECH_FOLDER + "/file_to_compile.dat")
#define COMPILE_HISTORY_LIST_FILE (std::string)(CUSTOM_COMPILER_CAECH_FOLDER + "/compiled_files_History.dat")
#define COMPILE_CONFIG (std::string)(CUSTOM_COMPILER_CAECH_FOLDER + "/compiled_links.dat")
#define COMPILE_CACHE (std::string)(CUSTOM_COMPILER_CAECH_FOLDER + "/cache_objects")
#define FILES_TO_CHECK (std::string)(CUSTOM_COMPILER_CAECH_FOLDER + "/FilesToCheck.dat")
#define INCLUDES_IN_FILES_LIST (std::string)(CUSTOM_COMPILER_CAECH_FOLDER + "/includesInFiles.dat")

// files types define
#define OBJECT_FILE_ENDING ".obj"

// keywords define
#define OPTIMIZE_LEVEL_KEYWORD "Optimize_level"
#define OUTPUT_FILE_KEYWORD "Output_file"
// #define SYSTEM_ADJUSTMENT_KEYWORD "allow_System_adjustment" // no need for system adjustments in native

// flag defines
#define DEBUGING_MODE_ON

// typedefs
typedef char OptimizeLevel;
typedef char (*func)(std::vector<std::string>);
typedef char t_ReturnMessage;