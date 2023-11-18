#include <vector>
#include <map>
#include <array>
//#include <thread>
#include <chrono>
#include <tuple>
#include <functional>
#include <iostream>
#include "Agents.hpp"
#include "ClassTypes.hpp"
#include "Board.hpp"

using namespace fastautomata::ClassTypes;

namespace fastautomata::Board {
    SimulatedBoard::SimulatedBoard(int width, int height, int layerCount)
    {
        this->width = width;
        this->height = height;
        this->layerCount = layerCount;
        this->agentSize = width * height;
        // this->layer_collisions = layer_collisions;
        this->board = new Agents::BaseAgent **[layerCount];
        for (int i = 0; i < layerCount; i++)
        {
            this->board[i] = new Agents::BaseAgent *[this->agentSize];
            for (int j = 0; j < this->agentSize; j++)
            {
                this->board[i][j] = nullptr;
            }
        }
        this->step_count = 0;

        this->color_map = std::map<std::string, std::array<int, 3>>();

        // add dead, alive and none
        this->addColor("Dead", std::array<int, 3>{100, 100, 100});
        this->addColor("Alive", std::array<int, 3>{150, 255, 150});
        this->addColor("None", std::array<int, 3>{0, 0, 0});

        this->step_instructions.push_back(SimulatedBoard::update_agents);
        this->step_instructions.push_back(SimulatedBoard::update_agents_end);
        this->step_instructions.push_back(SimulatedBoard::scheduled_delete);

        this->scheduled_delete_agents = std::vector<Agents::BaseAgent *>();

        // std::cout << "INFO: Created board with width: " << width << ", height: " << height << ", layers: " << layerCount << std::endl;

        this->layer_collisions = CollisionMap(layerCount);
    }

    SimulatedBoard::~SimulatedBoard()
    {
        // this->delete_this();
    }

    void SimulatedBoard::delete_this()
    {
        // clear board
        for (int i = 0; i < this->layerCount; i++)
        {
            // for (int j = 0; j < this->agentSize; j++)
            // {
            //     if (this->board[i][j] != nullptr)
            //     {
            //         delete this->board[i][j];
            //     }
            // }

            // only delete the pointer list, and let python take care of everything else
            delete[] this->board[i];
        }
        delete[] this->board;

        // clear all lists (do not delete tho)
        this->agents.clear();
        this->step_instructions.clear();
        this->on_add.clear();
        this->on_delete.clear();
        this->on_reset.clear();
        this->scheduled_delete_agents.clear();
        this->color_map.clear();
        this->color_map_count.clear();
    }

    int SimulatedBoard::getStepCount()
    {
        return this->step_count;
    }

    void SimulatedBoard::append_on_reset(std::function<void(SimulatedBoard *)> func)
    {
        this->on_reset.push_back(func);
    }

    void SimulatedBoard::append_on_add(std::function<void(Agents::BaseAgent *)> func)
    {
        this->on_add.push_back(func);
    }

    void SimulatedBoard::append_on_delete(std::function<void(Agents::BaseAgent *)> func)
    {
        this->on_delete.push_back(func);
    }

    int SimulatedBoard::getWidth()
    {
        return this->width;
    }

    int SimulatedBoard::getHeight()
    {
        return this->height;
    }

    int SimulatedBoard::getLayerCount()
    {
        return this->layerCount;
    }

    void SimulatedBoard::addColor(std::string name, std::array<int, 3> color)
    {
        this->color_map[name] = color;
        this->color_map_count[name] = 0;
    }

    void SimulatedBoard::step_instructions_add(std::function<void(SimulatedBoard *)> func)
    {
        this->step_instructions.push_back(func);
    }

    void SimulatedBoard::step_instructions_flush()
    {
        this->step_instructions.clear();
    }

    std::map<int, std::tuple<ClassTypes::CollisionType, Agents::BaseAgent *>> SimulatedBoard::getCollisions(ClassTypes::Pos pos, int layer, bool includeSelf)
    {
        if (pos.x < 0 || pos.y < 0 || pos.x >= this->width || pos.y >= this->height)
        {
            throw std::out_of_range("Position out of range when trying to check for collisions. (Pos given: " + pos.toString() + ")");
        }

        std::map<int, std::tuple<ClassTypes::CollisionType, Agents::BaseAgent *>> collisions;

        // std::cout << "INFO: Getting collisions for pos: " << pos.toString() << ", layer: " << std::to_string(layer) << ", includeSelf: " << includeSelf << std::endl;
        for (int searchLayer = 0; searchLayer < this->layerCount; searchLayer++)
        {
            if (searchLayer == layer)
            {
                // std::cout << "INFO: Skipping layer: " << std::to_string(searchLayer) << std::endl;
                if (includeSelf)
                {
                    auto agent = this->agent_get(pos, searchLayer);
                    bool agentExists = agent != nullptr;
                    // std::cout << "INFO: Agent exists: " << std::to_string(agentExists) << std::endl;
                    if (agent != nullptr)
                    {
                        collisions[searchLayer] = std::make_tuple(ClassTypes::CollisionType::SOLID, agent);
                    }
                    else
                    {
                        collisions[searchLayer] = std::make_tuple(ClassTypes::CollisionType::NONE, nullptr);
                    }
                }
                else
                {
                    collisions[searchLayer] = std::make_tuple(ClassTypes::CollisionType::NONE, nullptr);
                }
                // return NONE collision for self... This will ensure map has all objects.
                continue;
            }

            auto agent = this->agent_get(pos, searchLayer);
            if (agent != nullptr)
            {
                auto collision = layer_collisions.getCollision(layer, searchLayer);

                collisions[searchLayer] = std::make_tuple(collision, agent);
            }
            else
            {
                collisions[searchLayer] = std::make_tuple(ClassTypes::CollisionType::NONE, nullptr);
            }
        }

        return collisions;
    }

    /*
    ██    ██ ██████  ██████   █████  ████████ ██ ███    ██  ██████ 
    ██    ██ ██   ██ ██   ██ ██   ██    ██    ██ ████   ██ ██      
    ██    ██ ██████  ██   ██ ███████    ██    ██ ██ ██  ██ ██   ███ 
    ██    ██ ██      ██   ██ ██   ██    ██    ██ ██  ██ ██ ██    ██ 
     ██████  ██      ██████  ██   ██    ██    ██ ██   ████  ██████  
    */

    void SimulatedBoard::updateColor(std::string oldState, std::string newState)
    {
        // std::cout << "INFO: Updating color map. Old state: " << oldState << ", new state: " << newState << std::endl;

        this->color_map_count[oldState] -= 1;
        this->color_map_count[newState] += 1;
    }

    void SimulatedBoard::reset()
    {
        // Delete and recreate board
        for (int i = 0; i < this->layerCount; i++)
        {
            // for (int j = 0; j < this->agentSize; j++)
            // {
            //     if (this->board[i][j] != nullptr)
            //     {
            //         delete this->board[i][j];
            //     }
            // }
            delete[] this->board[i];
        }
        delete[] this->board;
        this->board = new Agents::BaseAgent **[this->layerCount];
        for (int i = 0; i < this->layerCount; i++)
        {
            this->board[i] = new Agents::BaseAgent *[this->agentSize];
            for (int j = 0; j < this->agentSize; j++)
            {
                this->board[i][j] = nullptr;
            }
        }

        // Reset step count
        this->step_count = 0;

        // Flush the agents
        this->agents.clear();

        // reset the count
        for (auto &kv : this->color_map_count)
        {
            kv.second = 0;
        }

        // Call on_reset functions
        for (auto func : this->on_reset)
        {
            func(this);
        }
    }

    void SimulatedBoard::step()
    {
        auto start = std::chrono::high_resolution_clock::now();
        // Call step instructions

        auto step = 0;

        for (auto func : this->step_instructions)
        {
            // std::cout << "INFO: Calling step instruction: " << step++ << std::endl;
            func(this);
        }

        // Increment step count
        this->step_count++;

        auto end = std::chrono::high_resolution_clock::now();

        // std::cout << "INFO: Step took: " << std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count() << "ms" << std::endl;
    }

    /*
     █████   ██████  ███████ ███    ██ ████████ ███████ 
    ██   ██ ██       ██      ████   ██    ██    ██      
    ███████ ██   ███ █████   ██ ██  ██    ██    ███████ 
    ██   ██ ██    ██ ██      ██  ██ ██    ██         ██ 
    ██   ██  ██████  ███████ ██   ████    ██    ███████ 
    */

    Agents::BaseAgent *SimulatedBoard::agent_get(Pos pos, int layer, bool wrap)
    {
        // std::cout << "INFO: Getting agent at pos: " << pos.toString() << ", layer: " << std::to_string(layer) << ", wrap: " << std::to_string(wrap) << std::endl;
        if (layer >= this->layerCount)
        {
            throw std::out_of_range("Layer out of range");
        }
        if (pos.x >= this->width || pos.y >= this->height || pos.x < 0 || pos.y < 0)
        {
            // std::cout << "WARNING: Position out of range. Pos: " << pos.toString() << ", width: " << std::to_string(this->width) << ", height: " << std::to_string(this->height) << std::endl;
            if (wrap)
            {
                // TODO use modulo instead of this
                int x = pos.x;
                int y = pos.y;

                if (pos.x < 0)
                {
                    x = this->width + pos.x;
                }
                if (pos.y < 0)
                {
                    y = this->height + pos.y;
                }

                if (pos.x >= this->width)
                {
                    x = pos.x % this->width;
                }
                if (pos.y >= this->height)
                {
                    y = pos.y % this->height;
                }

                pos = Pos(x, y);
                // std::cout << "INFO: Wrapped position. New pos: " << pos.toString() << std::endl;
            }
            else
            {
                return nullptr;
            }
        }

        // auto toReturn = this->board[layer][pos.toIndex(this->width)];
        // std::cout << "INFO: Returning agent at pos: " << pos.toString() << ", layer: " << std::to_string(layer) << ", wrap: " << std::to_string(wrap) << ". Agent: " << static_cast<void*>(toReturn) << std::endl;
        return this->board[layer][pos.toIndex(this->width)];
    }

    void SimulatedBoard::agent_add(Agents::BaseAgent *agent, bool allowOverrides)
    {
        auto existing = this->agent_get(agent->getPos(), agent->getLayer());

        // check if agent already exists
        if (existing != nullptr)
        {
            if (allowOverrides)
            {
                this->agent_remove(existing);
            }
            else
            {
                throw std::invalid_argument("Agent already exists at that position");
            }
        }

        // check if agent inherits from Agent
        Agents::Agent *simulatedAgent = dynamic_cast<Agents::Agent *>(agent);
        bool isSimulatedAgent = simulatedAgent != nullptr;

        // std::cout << "INFO: Adding agent. Si agent simulated? = " << isSimulatedAgent << ". Agent ID: " << agent->getId() << ". Simulated agent ID: " << simulatedAgent->getId() << ". Agent address: " << static_cast<void*>(agent) << std::endl;

        if (isSimulatedAgent)
        {
            this->agents.push_back(simulatedAgent);
        }

        // add agent to board
        this->board[agent->getLayer()][agent->getPos().toIndex(this->width)] = agent;

        // update color map
        color_map_count[agent->getState()] += 1;

        // call on_add functions
        for (auto func : this->on_add)
        {
            func(agent);
        }
    }

    void SimulatedBoard::agent_move(Agents::BaseAgent *agent, Pos posPrev, Pos posNew)
    {
        board[agent->getLayer()][posPrev.toIndex(this->width)] = nullptr;
        board[agent->getLayer()][posNew.toIndex(this->width)] = agent;
    }

    void SimulatedBoard::agent_move_layer(Agents::Agent *agent, int layerNew)
    {
        board[agent->getLayer()][agent->getPos().toIndex(this->width)] = nullptr;
        board[layerNew][agent->getPos().toIndex(this->width)] = agent;

        agent->changeLayer(layerNew);
    }

    void SimulatedBoard::agent_remove(Agents::BaseAgent *agent)
    {
        // check if agent is not already schedlued for deletion
        for (auto scheduledAgent : this->scheduled_delete_agents)
        {
            if (scheduledAgent == agent)
            {
                return;
            }
        }
        this->scheduled_delete_agents.push_back(agent);
    }

    /*
    ███████ ████████  █████  ████████ ██  ██████ 
    ██         ██    ██   ██    ██    ██ ██      
    ███████    ██    ███████    ██    ██ ██ 
         ██    ██    ██   ██    ██    ██ ██ 
    ███████    ██    ██   ██    ██    ██  ██████ 
    */

    /**
     * @brief Remove agents that have been scheduled for deletion.
     *
     * @param board The board (this is a static method)
     */
    void SimulatedBoard::scheduled_delete(SimulatedBoard *board)
    {
        for (auto agent : board->scheduled_delete_agents)
        {
            board->color_map_count[agent->getState()] -= 1;
            // std::cout << "INFO: Removing agent (id: " << std::to_string(agent->getId()) << "). Address; " << static_cast<void*>(agent) << std::endl;
            // remove agent from board
            board->board[agent->getLayer()][agent->getPos().toIndex(board->width)] = nullptr;

            // std::cout << "INFO: Removed agent from board" << std::endl;
            // check if agent is simulated Agent
            Agents::Agent *simulatedAgent = dynamic_cast<Agents::Agent *>(agent);
            if (simulatedAgent != nullptr)
            {
                // remove agent from agents
                for (int i = 0; i < board->agents.size(); i++)
                {
                    if (board->agents[i] == simulatedAgent)
                    {
                        board->agents.erase(board->agents.begin() + i);
                        // std::cout << "INFO: Removed agent from simulation loop." << std::endl;
                        break;
                    }
                }
            }

            // call on_delete functions
            for (auto func : board->on_delete)
            {
                func(agent);
            }

            if (board->python_on_delete != nullptr)
            {
                board->python_on_delete(agent);
            }
            else
            {
                delete agent;
            }

            // std::cout << "INFO: deleted agent no problems" << std::endl;
        }

        board->scheduled_delete_agents.clear();
    }

    /**
     * @brief A wrapper function that calls the step function of each agent
     *
     * @param board The board to update
     */
    void SimulatedBoard::update_agents(Board::SimulatedBoard *board)
    {
        // std::cout << "INFO: Updating agents" << std::endl;
        for (int i = 0; i < board->agents.size(); i++)
        {
            auto agent = board->agents[i];

            try
            {
                // std::cout << "INFO: Updating agent (id: " << std::to_string(agent->getId()) << "). Address: " << static_cast<void*>(agent) << std::endl;
                agent->step();
                // std::cout << "INFO: Finished" << std::endl;
            }
            catch (const std::exception &e)
            {
                std::cout << "ERROR: When stepping through agents: " << e.what() << std::endl;
            }
        }
        // std::cout << "INFO: Updating agents finished" << std::endl;

        // const int num_threads = std::thread::hardware_concurrency();

        // // Calculate the number of agents per thread
        // int agents_per_thread = board->agents.size() / num_threads;

        // std::vector<std::thread> threads(num_threads);

        // for (int t = 0; t < num_threads; t++) {
        //     threads[t] = std::thread([&, t]() {
        //         // Calculate the start and end indices for this thread
        //         int start = t * agents_per_thread;
        //         int end = (t == num_threads - 1) ? board->agents.size() : start + agents_per_thread;

        //         for (int i = start; i < end; i++) {
        //             auto agent = board->agents[i];

        //             try {
        //                 agent->step();
        //             } catch(const std::exception& e) {
        //                 std::cout << "ERROR: When stepping through agents: " << e.what() << std::endl;
        //             }
        //         }
        //     });
        // }

        // // Wait for all threads to finish
        // for (auto& thread : threads) {
        //     thread.join();
        // }
    }

    /**
     * @brief A wrapper function that calls the step_end function of each agent
     *
     * @param board The board to update
     */
    void SimulatedBoard::update_agents_end(Board::SimulatedBoard *board)
    {
        // std::cout << "INFO: Updating agents, step: end" << std::endl;
        for (auto agent : board->agents)
        {
            agent->step_end();
        }
        // std::cout << "INFO: Finished updating agents, step: end. Updated: " << board->agents.size() << std::endl;
    }

    /// @brief Create a random color
    /// @return A random color in rgb format
    std::array<int, 3> SimulatedBoard::getRandomColor()
    {
        return std::array<int, 3>{rand() % 255, rand() % 255, rand() % 255};
    }
}