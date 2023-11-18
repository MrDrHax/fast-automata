#pragma once

#include <vector>
#include <map>
#include <thread>
#include <chrono>
#include <tuple>
#include <functional>
#include <iostream>
#include "Agents.hpp"
#include "ClassTypes.hpp"

using namespace fastautomata::ClassTypes;

namespace fastautomata::Board {
    /**
     * @brief A board that can be simulated
     * 
     */
    class SimulatedBoard
    {
        /*
        ██    ██  █████  ██████  ██  █████  ██████  ██      ███████ ███████ 
        ██    ██ ██   ██ ██   ██ ██ ██   ██ ██   ██ ██      ██      ██      
        ██    ██ ███████ ██████  ██ ███████ ██████  ██      █████   ███████ 
         ██  ██  ██   ██ ██   ██ ██ ██   ██ ██   ██ ██      ██           ██ 
          ████   ██   ██ ██   ██ ██ ██   ██ ██████  ███████ ███████ ███████ 
                                                                          
                                                                            
        */
        private:
        int width;
        int height;
        int layerCount;
        int agentSize;

        /**
         * @brief A representation of the board ([layer][x*y][agent])
         * 
         */
        Agents::BaseAgent*** board;

        /**
         * @brief The agents that will get updated each step
         * 
         */
        std::vector<Agents::Agent*> agents;

        /**
         * @brief The current step (counter) in the simulation
         * 
         */
        int step_count;


        public:
        /**
         * @brief The collisions that will be checked when repositioning agents
         * 
         */
        CollisionMap layer_collisions;

        /**
         * @brief A list of functions to call on each step
         * 
         */
        std::vector<std::function<void(SimulatedBoard*)>> step_instructions;

        /**
         * @brief A dictionary of colors to use for automatas
         * 
         */
        std::map<std::string, std::array<int, 3>> color_map;

        /**
         * @brief A dictionary that holds info about the time that it takes to get objects. 
         * 
         */
        std::map<std::string, int> color_map_count; 

        /**
         * @brief List of functions to call on reset
         * 
         */
        std::vector<std::function<void(SimulatedBoard*)>> on_reset;

        /**
         * @brief List of functions to call when a new agent is added
         * 
         */
        std::vector<std::function<void(Agents::BaseAgent*)>> on_add;

        /**
         * @brief List of functions to call when an agent is deleted
         * 
         */
        std::vector<std::function<void(Agents::BaseAgent*)>> on_delete;

        /**
         * @brief Python is... special...
         * 
         */
        std::function<void(Agents::BaseAgent*)> python_on_delete;

        /**
         * @brief A list of agents that will be deleted at the end of the step
         * 
         */
        std::vector<Agents::BaseAgent*> scheduled_delete_agents;

        /*
         ██████  ██████  ███    ██ ███████ ████████ ██████  ██    ██  ██████ ████████  ██████  ██████  ███████ 
        ██      ██    ██ ████   ██ ██         ██    ██   ██ ██    ██ ██         ██    ██    ██ ██   ██ ██      
        ██      ██    ██ ██ ██  ██ ███████    ██    ██████  ██    ██ ██         ██    ██    ██ ██████  ███████ 
        ██      ██    ██ ██  ██ ██      ██    ██    ██   ██ ██    ██ ██         ██    ██    ██ ██   ██      ██ 
         ██████  ██████  ██   ████ ███████    ██    ██   ██  ██████   ██████    ██     ██████  ██   ██ ███████ 
        */

        /**
         * @brief Construct a new Simulated Board object
         * 
         * @param width 
         * @param height 
         * @param layerCount 
         */
        SimulatedBoard(int width, int height, int layerCount);

        /**
         * @brief Destroy the Simulated Board object
         * 
         */
        ~SimulatedBoard();

        void delete_this();

        /*
         ██████  ███████ ████████         ██     ███████ ███████ ████████ 
        ██       ██         ██           ██      ██      ██         ██    
        ██   ███ █████      ██          ██       ███████ █████      ██    
        ██    ██ ██         ██         ██             ██ ██         ██    
         ██████  ███████    ██        ██         ███████ ███████    ██                              
        */

        int getStepCount();

        void append_on_reset(std::function<void(SimulatedBoard *)> func);

        void append_on_add(std::function<void(Agents::BaseAgent *)> func);

        void append_on_delete(std::function<void(Agents::BaseAgent *)> func);

        /**
         * @brief Get the Width object
         * 
         * @return int 
         */
        int getWidth();

        /**
         * @brief Get the Height object
         * 
         * @return int 
         */
        int getHeight();

        /**
         * @brief Get the Layer Count object
         * 
         * @return int 
         */
        int getLayerCount();

        /**
         * @brief Add a color to the simulation (state)
         * 
         * @param name The state
         * @param color The color that will be used
         */
        void addColor(std::string name, std::array<int, 3> color);

        /**
         * @brief Add an instruction to the steps that will be executed each step
         * 
         * @param func 
         */
        void step_instructions_add(std::function<void(SimulatedBoard *)> func);

        /**
         * @brief remove all the step instructions
         */
        void step_instructions_flush();

        /**
         * @brief Get the Collisions of an agent from given layer. Returns a map of layers to collision types.
         * 
         * @param pos The position to check collisions for
         * @param layer The layer from where to check collisions 
         * @param includeSelf If true, returns it's own layer as well
         * @return std::map<int, std::tuple<ClassTypes::CollisionType, Agents::BaseAgent*>> 
         */
        std::map<int, std::tuple<ClassTypes::CollisionType, Agents::BaseAgent *>> getCollisions(ClassTypes::Pos pos, int layer = 0, bool includeSelf = true);

        /*
        ██    ██ ██████  ██████   █████  ████████ ██ ███    ██  ██████  
        ██    ██ ██   ██ ██   ██ ██   ██    ██    ██ ████   ██ ██       
        ██    ██ ██████  ██   ██ ███████    ██    ██ ██ ██  ██ ██   ███ 
        ██    ██ ██      ██   ██ ██   ██    ██    ██ ██  ██ ██ ██    ██ 
         ██████  ██      ██████  ██   ██    ██    ██ ██   ████  ██████  
        */

        /**
         * @brief Update the index of a new and old state in the color map. This assumes you did a color check first
         * 
         * @param oldState the state that got replaced
         * @param newState the state that replaced the old state
         */
        void updateColor(std::string oldState, std::string newState);

        void reset();

        /**
         * @brief Step through an iteration of the simulation
         * 
         * The steps to run are defined by step_instructions
         * 
         */
        void step();

        /*
         █████   ██████  ███████ ███    ██ ████████ ███████ 
        ██   ██ ██       ██      ████   ██    ██    ██      
        ███████ ██   ███ █████   ██ ██  ██    ██    ███████ 
        ██   ██ ██    ██ ██      ██  ██ ██    ██         ██ 
        ██   ██  ██████  ███████ ██   ████    ██    ███████ 
        */

        /**
         * @brief Get an agent at a position
         * 
         * @param pos The position to get the agent from
         * @param layer [optional] The layer to get the agent from [default: 0]
         * @param wrap [optional] Whether to wrap the position if it is out of bounds [default: false]
         * @return Agents::BaseAgent* The agent at the position. Returns nullptr if no agent is found.
         */
        Agents::BaseAgent *agent_get(Pos pos, int layer = 0, bool wrap = false);

        /**
         * @brief Add an agent to the board
         * 
         * @param agent 
         * @param allowOverrides 
         */
        void agent_add(Agents::BaseAgent *agent, bool allowOverrides = false);

        /**
         * @brief Move an agent to a new position. 
         * 
         * WARNING: Does not check if the position is valid. It assumes you already checked
         * 
         * @param agent The agent to move
         * @param posPrev The previous position of the agent
         * @param posNew The new position of the agent
         */
        void agent_move(Agents::BaseAgent *agent, Pos posPrev, Pos posNew);

        void agent_move_layer(Agents::Agent *agent, int layerNew);

        /**
         * @brief remove an agent from board. Deletes it afterwards.
         * 
         * @param agent The agent to delete
         */
        void agent_remove(Agents::BaseAgent *agent);

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
        static void scheduled_delete(SimulatedBoard *board);

        /**
         * @brief A wrapper function that calls the step function of each agent
         * 
         * @param board The board to update
         */
        static void update_agents(Board::SimulatedBoard *board);

        /**
         * @brief A wrapper function that calls the step_end function of each agent
         * 
         * @param board The board to update
         */
        static void update_agents_end(Board::SimulatedBoard *board);

        /// @brief Create a random color
        /// @return A random color in rgb format
        static std::array<int, 3> getRandomColor();
    };
}