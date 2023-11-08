#include "Agents.hpp"
#include "Board.hpp"
#include <pybind11/pybind11.h>

namespace fastautomata::Agents {
    /*
    ██████   █████  ███████ ███████      █████   ██████  ███████ ███    ██ ████████ 
    ██   ██ ██   ██ ██      ██          ██   ██ ██       ██      ████   ██    ██    
    ██████  ███████ ███████ █████       ███████ ██   ███ █████   ██ ██  ██    ██    
    ██   ██ ██   ██      ██ ██          ██   ██ ██    ██ ██      ██  ██ ██    ██    
    ██████  ██   ██ ███████ ███████     ██   ██  ██████  ███████ ██   ████    ██                                                                                                                            
    */

    int BaseAgent::current_id = 0;

    BaseAgent::BaseAgent()
    {
        this->id = current_id++;
    }

    BaseAgent::BaseAgent(Board::SimulatedBoard* board, Pos pos, std::string state, int layer, bool allowOverriding)
    {
        this->board = board;
        this->pos = pos;
        this->layer = layer;
        this->state = state;
        this->id = current_id++;

        this->board->agent_add(this, allowOverriding);
    }

    Pos BaseAgent::getPos()
    {
        return this->pos;
    }

    int BaseAgent::getId()
    {
        return this->id;
    }

    std::string BaseAgent::getState()
    {
        return this->state;
    }

    int BaseAgent::getLayer()
    {
        return this->layer;
    }

    void BaseAgent::kill()
    {
        this->board->agent_remove(this);
    }

    bool BaseAgent::checkCollisions(CollisionType type, Pos seachIn)
    {
        // std::cout << "Checking collisions for agent (id: " << std::to_string(this->getId()) << ") in pos: " << seachIn.toString() << std::endl;
        bool searchSelf = !(seachIn == this->pos);
        // std::cout << "Search self: " << std::to_string(searchSelf) << std::endl;
        auto collisions = this->board->getCollisions(seachIn, this->layer, searchSelf);

        // std::cout << "Collisions found: " << std::to_string(collisions.size()) << std::endl;
        for (auto coll: collisions)
        {
            auto coltype = std::get<0>(coll.second);
            // std::cout << "Collision: " << std::to_string(coltype) << std::endl;
            if (coltype == type)
            {
                return true;
            }
        }

        return false;
    }

    /*
     █████   ██████  ███████ ███    ██ ████████ 
    ██   ██ ██       ██      ████   ██    ██    
    ███████ ██   ███ █████   ██ ██  ██    ██    
    ██   ██ ██    ██ ██      ██  ██ ██    ██    
    ██   ██  ██████  ███████ ██   ████    ██    
    */

    Agent::Agent() : BaseAgent()
    {

    }

    Agent::Agent(Board::SimulatedBoard* board, Pos pos, std::string state, int layer, bool allowOverriding) 
    {
        this->board = board;
        this->pos = pos;
        this->layer = layer;
        this->state = state;

        if (this->board->color_map.find(state) == this->board->color_map.end())
        {
            std::cout << "WARNING: State '" << state << "' does not exist in the color map. It will be added with a random color." << std::endl;
            this->board->addColor(state, this->board->getRandomColor());
        }

        this->board->agent_add(this, allowOverriding);
    }

    void Agent::step()
    {
        // std::cout << "Agent (id: " << std::to_string(this->getId()) << ") is stepping. Function did not get overriden!!!! " << std::endl;
    }

    void Agent::step_end()
    {
        bool gotUpdated = false;

        // if position has been updated, move the agent
        if (pos_next)
        {
            // std::cout << "Moving agent (id: " << std::to_string(this->getId()) << ") to pos: " << (*this->pos_next).toString() << std::endl;
            // check if there are any collisions in current pos (of type SOLID)
            bool collision = checkCollisions(CollisionType::SOLID, *this->pos_next);
            
            // std::cout << "Collision: " << std::to_string(collision) << std::endl;
            // only move if there are no collisions
            if (!collision)
            {
                // std::cout << "No problems found for agent id: " << std::to_string(this->getId()) << " to pos: " << (*this->pos_next).toString() << std::endl;
                board->agent_move(this, this->pos,*this->pos_next);
                this->pos = *this->pos_next;
                gotUpdated = true;
                // std::cout << "Agent was moved" << std::endl;
            }
            else
            {
                std::cout << "WARNING: Cannot move agent (id: " << std::to_string(this->getId()) << ") to pos: " << (*this->pos_next).toString() << " because it's occupied (a SOLID collision detected)." << std::endl;
            }

            // reset the next pos
            this->pos_next = nullptr;
        }

        // if state has been updated, update the state
        if (state_next)
        {
            // update the colors in board
            this->board->updateColor(this->state, *this->state_next);

            // update the state
            this->state = *this->state_next;
            this->state_next = nullptr;
            gotUpdated = true;
        }

        // call on_update functions if there were any updates
        if (gotUpdated)
        {
            for (auto func : this->on_update)
            {
                func(this);
            }
        }
    }

    void Agent::append_on_update(std::function<void(Agent*)> func)
    {
        this->on_update.push_back(func);
    }

    void Agent::setPos(Pos pos)
    {
        this->pos_next = std::make_unique<Pos>(pos);
    }

    void Agent::setState(std::string state)
    {
        if (this->board->color_map.find(state) == this->board->color_map.end())
        {
            // std::cout << "WARNING: State '" << state << "' does not exist in the color map. It will be added with a random color." << std::endl;
            this->board->addColor(state, this->board->getRandomColor());
        }
        this->state_next = std::make_unique<std::string>(state);
    }

    void Agent::changeLayer(int layer)
    {
        //this->board->agent_move_layer(this, this->layer, layer);
        this->layer = layer;
    }

    std::vector<BaseAgent*> Agent::get_neighbors(int radius, bool wrap, int layer)
    {
        if (layer == -1)
        {
            layer = this->layer;
        }
        
        // std::cout << "Getting neighbors for agent (id: " << std::to_string(this->getId()) << ") in pos: " << this->pos.toString() << " with radius: " << std::to_string(radius) << std::endl;
        std::vector<BaseAgent*> neighbors;
        neighbors.reserve(pow(radius * 2 + 1, 2));

        // always return top left to bottom right
        for (int j = this->pos.y + radius; j >= this->pos.y - radius ; j--)
        {
            for (int i = this->pos.x - radius; i <= this->pos.x + radius; i++)
            {
                neighbors.push_back(this->board->agent_get(Pos(i,j), this->layer, wrap));
            }
        }

        return neighbors;
    }

    std::string Agent::toString()
    {
        return "Agent (id: " + std::to_string(this->getId()) + ", pos: " + this->pos.toString() + ", state: " + this->state + ")";
    }

    std::string Agent::objInfo()
    {
        return "<fastautomata_clib.Agent id='" + std::to_string(this->getId()) + "'>";
    }

    void PyAgent::step()
    {
        PYBIND11_OVERLOAD_PURE(
            void,
            Agent,
            step
        );
    }

    void PyAgent::step_end()
    {
        PYBIND11_OVERLOAD(
            void,
            Agent,
            step_end
        );
    }

    void PyAgent::kill()
    {
        PYBIND11_OVERLOAD(
            void,
            Agent,
            kill
        );
    }

    void BaseAgentPy::kill()
    {
        PYBIND11_OVERLOAD(
            void,
            BaseAgent,
            kill
        );
    }
}