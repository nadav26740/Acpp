#pragma once
#include <iostream>
#include <string>
#include <fstream>

// third party libs
#include "../nlohmann/json.hpp"

// define libs
#include "../File_Defines.hpp"

using json = nlohmann::json;

namespace acpp
{
    // {"Output_file":"release/out", "Optimize_level": "3", "allow_System_adjustment": "True"}
    struct Config_json
    {
        std::string Output_file;
        int optimize_level;
        bool DebugMode;
    };

    struct Config_path
    {
        std::string path;
    };

    class Config
    {
    private:
        Config_json data;
        template<class T> void ExtractDataFromJson(T);

    public:
        Config(Config_path File_path); // reading the config data from file path
        Config(std::string Json_data); // creating config from json data
        Config(); // Creating default config
        ~Config(); // destractor
        const std::string to_string();
    };
}