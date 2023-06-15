#pragma once
#include <iostream>
#include <map>
#include <string>
#include <vector>
#include <memory>

typedef char (*func)(std::vector<std::string>);
typedef char t_ReturnMessage;
namespace acpp
{
    std::unique_ptr<std::map<std::string, func>> func_dict;

    void initMap();
    func GetFunc(std::string func_name);
    t_ReturnMessage print_help(std::vector<std::string> args);
    t_ReturnMessage print_Func_not_found(std::vector<std::string> args);
}