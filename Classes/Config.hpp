#pragma once
#include <iostream>
#include <string>
#include <fstream>

// third party libs
#include <nlohmann/json.hpp>

// define libs
#include "File_Defines.hpp"

namespace acpp
{
    struct Config_path
    {
        std::string path;
    };

    class Config
    {
    private:
        std::string m_Output_file;
        OptimizeLevel m_OptimizeLevel;

    public:
        Config(Config_path File_path); // reading the config data from file path
        Config(std::string Json_data); // creating config from json data
        Config(); // Creating default config
        ~Config(); // destractor

    };
}