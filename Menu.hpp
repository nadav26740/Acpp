#pragma once
#include <iostream>
#include <map>
#include <string>
#include <vector>
#include <memory>

// included files
#include "Classes/Config.hpp"

// third party
#include "third_party/md5_hasher.hpp"

// defines
#include "File_Defines.hpp"

namespace acpp
{
    static std::unique_ptr<std::map<std::string, func>> func_dict;
    static std::map<std::string, func> func_dict2;
    
    void initMap();

    /// @brief Finding by command string function to do the command
    /// @param func_name
    /// @return Function Pointer
    func GetFunc(std::string func_name);

    /// @brief Printing all the available Commands
    /// @param args 
    /// @return Success status code
    Return_codes print_help(std::vector<std::string> args);

    /// @brief Printing error Wrong args message
    /// @param args 
    /// @return Failed Status code
    Return_codes print_Func_not_found(std::vector<std::string> args);

    /// @brief For test checking
    /// @param args 
    /// @return Status Code
    Return_codes dummy_ShowConfig(std::vector<std::string> args);

    /// @brief Getting path and creating/adding code file paths to the file list
    /// @param args 
    /// @return Status Code
    Return_codes add_new_file(std::vector<std::string> args);
}