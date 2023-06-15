#pragma once
#include <iostream>
#include <map>
#include <string>
#include <vector>

typedef char (*func)(std::vector<std::string>);
typedef char t_ReturnMessage;
namespace acpp
{
    const std::map<std::string, func> func_dict{{"help", &print_help}};
    func GetFunc(std::string func_name);
    t_ReturnMessage print_help(std::vector<std::string> args);
    t_ReturnMessage print_Func_not_found(std::vector<std::string> args);
}