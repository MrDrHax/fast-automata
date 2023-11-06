/**
 * @file Agents.hpp
 * @author MrDrHax (alexfh2001@gmail.com)
 * @brief Defines agents and types
 * @version 0.1
 * @date 2023-11-04
 * 
 * @copyright Copyright (c) 2023
 * 
 */

#pragma once

#include "ClassTypes.hpp"
#include <memory>
#include <functional>
#include <math.h>
#include <iostream>

using namespace fastautomata::ClassTypes;

namespace fastautomata::Board {
    class SimulatedBoard;
}

namespace fastautomata::Agents{
    /**
     * @brief A base agent. it is static, you can define to use for example, in walls.
     * 
     */
    class BaseAgent
    {
        private:
        static int current_id;
        int id;

        protected:
        /**
         * @brief The position in which the agent is located. Do not edit directly!!!
         * 
         */
        Pos pos;

        /**
         * @brief The located layer
         * 
         */
        int layer;

        /**
         * @brief The current state of the cell. Do not edit directly!!!
         * 
         */
        std::string state;

        public:


        /**
         * @brief A reference to the board. Once defined, should not be edited.
         * 
         */
        Board::SimulatedBoard* board;


        BaseAgent();

        /**
         * @brief Construct a new Base Agent object
         * 
         * @param board Reference to the board
         * @param pos The start position
         * @param state The current state to define
         * @param layer [Optional] What layer will the agent be located (default: 0)
         * @param allowOverriding [Optional] When positioning in board, can it delete the other agent? (default: false)
         */
        BaseAgent(Board::SimulatedBoard* board, Pos pos, std::string state, int layer = 0, bool allowOverriding = false);
        /**
         * @brief Get the Pos object
         * 
         * @return Pos 
         */
        Pos getPos();

        /**
         * @brief Get the Id
         * 
         * @return int 
         */
        int getId();

        /**
         * @brief Get the Layer
         * 
         * @return int 
         */
        int getLayer();

        std::string getState();

        /**
         * @brief Delete the agent from the board. 
         * 
         */
        void kill();

        /**
         * @brief Check if there is a collision in the position
         * 
         * @param type The type of collision
         * @param seachIn The position to search in
         * @return true if there was a collision
         * @return false if there was not a collision
         */
        bool checkCollisions(CollisionType type, Pos seachIn);
        virtual ~BaseAgent() = default;
    };

    /**
     * @brief An agent that can be used on a board. This agent is simulated.
     * 
     */
    class Agent: public BaseAgent
    {
        private:
        /**
         * @brief Defines a state that will get changed at the end of the step.
         * 
         */
        std::unique_ptr<std::string> state_next = nullptr;
        /**
         * @brief Defines a position where it will move towards. 
         * 
         */
        std::unique_ptr<Pos> pos_next = nullptr;

        public:
        Agent();
        Agent(Board::SimulatedBoard* board, Pos pos, std::string state, int layer, bool allowOverriding);
           

        /**
         * @brief Callback functions that will be called at the end of the step when the cell gets updated.
         * 
         */
        std::vector<std::function<void(Agent*)>> on_update;

        void append_on_update(std::function<void(Agent*)> func);

        /**
         * @brief A step function that gets called every step by default. Can be changed.
         * 
         */
        virtual void step();

        /**
         * @brief A step function that gets called at the end of every step by default. Can be changed.
         * 
         */
        virtual void step_end();

        /**
         * @brief Queue a state change. Will be changed at the end of the step.
         * 
         * @param pos 
         */
        void setPos(Pos pos);

        void changeLayer(int layer);

        /**
         * @brief Set the State object
         * 
         * @param state 
         */
        void setState(std::string state);

        /**
         * @brief Get the neighbors list. The full list of neighbors is defined by the radius. It will always return a list of size (radius * 2 + 1)^2. If there is no agent, or out of bounds, returns nullptr
         * 
         * @param radius the search distance. 
         * @param wrap if the element is out of bounds, will it wrap around? (default: false)
         * @param layer the layer to search in. If -1, will search in it's layer.
         * @return std::vector<BaseAgent*> 
         */
        std::vector<BaseAgent*> get_neighbors(int radius, bool wrap = false, int layer = -1);

        std::string toString();
        std::string objInfo();

        virtual ~Agent() = default;
    };

    class PyAgent: public Agent
    {
        public:
        using Agent::Agent;

        void step() override;
        void step_end() override;
    };
}