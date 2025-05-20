#include <fstream>
#include <iostream>
#include <map>
#include <string>
#include <vector>

#include "csv.hpp"

using namespace std;
using namespace csv;

bool FILTER = false;
vector<string> VERSION = {};
vector<string> CATEGORY = {};
vector<string> DIFFICULTY = {};
vector<string> LEVEL = {};

void load_env() {
    // read .env file
    ifstream env_file(".env");
    if (!env_file.is_open()) {
        cerr << "無法開啟設定檔" << endl;
        return;
    }

    // store key-value pairs
    map<string, string> env_map;
    string line;
    while (getline(env_file, line)) {
        size_t pos = line.find('=');
        if (pos != string::npos) {
            string key = line.substr(0, pos);
            string value = line.substr(pos + 1);
            env_map[key] = value;
        }
    }
    env_file.close();

    // load env variables
    if (env_map.find("FILTER") != env_map.end()) {
        FILTER = (env_map["FILTER"] == "True");
    }

    if (env_map.find("VERSION") != env_map.end()) {
        string versions = env_map["VERSION"];
        size_t start = 0;
        size_t pos = 0;
        while ((pos = versions.find(',')) != string::npos) {
            VERSION.push_back(versions.substr(start, pos - start));
            start = pos + 1;
        }
    }

    if (env_map.find("CATEGORY") != env_map.end()) {
        string categories = env_map["CATEGORY"];
        size_t start = 0;
        size_t pos = 0;
        while ((pos = categories.find(',')) != string::npos) {
            CATEGORY.push_back(categories.substr(start, pos - start));
            start = pos + 1;
        }
    }

    if (env_map.find("DIFFICULTY") != env_map.end()) {
        string difficulties = env_map["DIFFICULTY"];
        size_t start = 0;
        size_t pos = 0;
        while ((pos = difficulties.find(',')) != string::npos) {
            DIFFICULTY.push_back(difficulties.substr(start, pos - start));
            start = pos + 1;
        }
    }

    if (env_map.find("LEVEL") != env_map.end()) {
        string levels = env_map["LEVEL"];
        size_t start = 0;
        size_t pos = 0;
        while ((pos = levels.find(',')) != string::npos) {
            LEVEL.push_back(levels.substr(start, pos - start));
            start = pos + 1;
        }
    }
}

int main() {
    csv::CSVReader reader("sheet_data.csv");
    for (auto& row : reader) {
    }
}
