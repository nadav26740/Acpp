#include <string>
#include <iostream>
#include <memory>
#include <vector>
#include <map>
#include <optional>


namespace acpp
{
    class globalConfig 
    {

    public:
        static std::string get_system_os();

        static std::map<std::string, std::string> Config;
    };
};