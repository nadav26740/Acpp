#include "Config.hpp"

template<class T>
void acpp::Config::ExtractDataFromJson(T js)
{
    json json_Data = json::parse(js);
    this->data.Output_file = json_Data[OUTPUT_FILE_KEYWORD];

    this->data.optimize_level = json_Data[OPTIMIZE_LEVEL_KEYWORD];
}

acpp::Config::Config(Config_path File_path)
{
    ExtractDataFromJson(std::ifstream(File_path.path));
}

acpp::Config::Config(std::string Json_data)
{
    ExtractDataFromJson(Json_data);
}

acpp::Config::Config()
{
}

acpp::Config::~Config()
{
}

const std::string acpp::Config::to_string()
{
    std::string str = " ";
    str = "Output: " + this->data.Output_file + 
    " Optimize Level: " + std::to_string(this->data.optimize_level);

    return str;
}
