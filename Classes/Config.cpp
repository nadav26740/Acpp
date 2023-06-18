#include "Config.hpp"

void acpp::Config::ExtractDataFromJson()
{
    json data = json::parse(std::string());
    data[OUTPUT_FILE_KEYWORD];
}