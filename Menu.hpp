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
    
    void initMap();
    func GetFunc(std::string func_name);
    t_ReturnMessage print_help(std::vector<std::string> args);
    t_ReturnMessage print_Func_not_found(std::vector<std::string> args);
    t_ReturnMessage dummy_ShowConfig(std::vector<std::string> args);
}