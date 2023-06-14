#include <iostream>
#include <vector>
#include <string>
#include <memory>

#define DEBUGING_MODE_ON

#define CUSTOM_COMPILER_CAECH_FOLDER (std::string)(".AutoCompiler")
#define CODES_FILES_LIST_FILE (std::string)(CUSTOM_COMPILER_CAECH_FOLDER + "/file_to_compile.dat")
#define COMPILE_HISTORY_LIST_FILE (std::string)(CUSTOM_COMPILER_CAECH_FOLDER + "/compiled_files_History.dat")
#define COMPILE_CONFIG (std::string)(CUSTOM_COMPILER_CAECH_FOLDER + "/compiled_links.dat")
#define COMPILE_CACHE (std::string)(CUSTOM_COMPILER_CAECH_FOLDER + "/cache_objects")
#define FILES_TO_CHECK (std::string)(CUSTOM_COMPILER_CAECH_FOLDER + "/FilesToCheck.dat")
#define INCLUDES_IN_FILES_LIST (std::string)(CUSTOM_COMPILER_CAECH_FOLDER + "/includesInFiles.dat")

#define OBJECT_FILE_ENDING ".obj"

#define OPTIMIZE_LEVEL_KEYWORD "Optimize_level"
#define OUTPUT_FILE_KEYWORD "Output_file"
#define SYSTEM_ADJUSTMENT_KEYWORD "allow_System_adjustment"


int main(int argc, char *argv[])
{
  std::cout << "Starting.." << std::endl;

  // debuging
#ifdef DEBUGING_MODE_ON
 
  std::cout << "Debug: Cache folder - " << CUSTOM_COMPILER_CAECH_FOLDER << std::endl
  << "Debug: File_list - " << CODES_FILES_LIST_FILE << std::endl
  << "Debug: history file list - " << COMPILE_HISTORY_LIST_FILE << std::endl
  << "Debug: config_path - " << COMPILE_CONFIG << std::endl
  << "Debug: cache Objects folder - " << COMPILE_CACHE << std::endl
  << "Debug: Files to check file - " << FILES_TO_CHECK << std::endl
  << "Dubug: Includes files list - " << INCLUDES_IN_FILES_LIST << std::endl << std::endl
  << "Debug: ======== Config keywords ========" << std::endl
  << "Debug: Optimize keyword - " << OPTIMIZE_LEVEL_KEYWORD << std::endl
  << "Debug: Output file keyword - " << OUTPUT_FILE_KEYWORD << std::endl
  << "Debug: System adjustment keyword - " << SYSTEM_ADJUSTMENT_KEYWORD << std::endl;

#endif

// creating a ptr of vector to hold all the args
  std::unique_ptr<std::vector<std::string>> args = std::make_unique<std::vector<std::string>>();

// inserting all the args into the vector
  for (int i = 0; i < argc; i++)
  {
    args->push_back(argv[i]);
  }
  return 0;
}
