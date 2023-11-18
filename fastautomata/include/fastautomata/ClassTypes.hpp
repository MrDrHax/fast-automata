/**
 * @file ClassTypes.cpp
 * @author MrDrHax (alexfh2001@gmail.com)
 * @brief The Base types used in fastautomata
 * @version 0.1
 * @date 2023-11-03
 * 
 * @copyright Copyright (c) 2023
 * 
 */

#pragma once

#include <math.h>
#include <stdexcept>
#include <vector>
#include <map>
#include <string> 

namespace fastautomata::ClassTypes{
    /**
     * @brief A 2D position
     * Can be treated as Vector2Int
     */
    class Pos
    {
        public:
        int x;
        int y;

        Pos()
        {
            this->x = 0;
            this->y = 0;
        }

        Pos(int x, int y)
        {
            this->x = x;
            this->y = y;
        }

        // special functions
        Pos copy()
        {
            return Pos(this->x, this->y);
        }

        int toIndex(int width)
        {
            return this->x + this->y * width;
        }

        // Vector functions
        float magnitude()
        {
            return sqrt(pow(this->x, 2) + pow(this->y, 2));
        }

        Pos normalize()
        {
            return Pos(this->x / this->magnitude(), this->y / this->magnitude());
        }

        // Operators
        Pos operator+(Pos pos)
        {
            return Pos(this->x + pos.x, this->y + pos.y);
        }

        Pos operator-(Pos pos)
        {
            return Pos(this->x - pos.x, this->y - pos.y);
        }

        Pos operator*(Pos pos)
        {
            return Pos(this->x * pos.x, this->y * pos.y);
        }

        Pos operator/(Pos pos)
        {
            return Pos(this->x / pos.x, this->y / pos.y);
        }

        Pos operator%(Pos pos)
        {
            return Pos(this->x % pos.x, this->y % pos.y);
        }

        Pos operator+=(Pos pos)
        {
            this->x += pos.x;
            this->y += pos.y;
            return *this;
        }

        Pos operator-=(Pos pos)
        {
            this->x -= pos.x;
            this->y -= pos.y;
            return *this;
        }

        Pos operator*=(Pos pos)
        {
            this->x *= pos.x;
            this->y *= pos.y;
            return *this;
        }

        Pos operator/=(Pos pos)
        {
            this->x /= pos.x;
            this->y /= pos.y;
            return *this;
        }

        Pos operator%=(Pos pos)
        {
            this->x %= pos.x;
            this->y %= pos.y;
            return *this;
        }

        bool operator==(Pos pos)
        {
            return this->x == pos.x && this->y == pos.y;
        }

        bool operator!=(Pos pos)
        {
            return this->x != pos.x || this->y != pos.y;
        }

        bool operator>(Pos pos)
        {
            return this->magnitude() > pos.magnitude();
        }

        bool operator<(Pos pos)
        {
            return this->magnitude() < pos.magnitude();
        }

        std::string toString()
        {
            return "(" + std::to_string(this->x) + ", " + std::to_string(this->y) + ")";
        }
    };

    /**
     * @brief Describes the type of collisions a tile can have
     * 
     */
    enum CollisionType
    {
        /**
         * @brief No collision, agents will move to that pos
         * 
         */
        NONE,
        /**
         * @brief Wall collision, cannot move an agent if there is a solid collision to that pos
         * 
         */
        SOLID,
        /**
         * @brief Trigger collision, can move an agent if there is a trigger collision to that pos (as long as not in the same layer)
         * 
         */
        TRIGGER
    };

    class CollisionList
    {
        std::map<int, CollisionType> collisions;

        public:
        CollisionList()
        {
            this->collisions = std::map<int, CollisionType>();
        }

        CollisionType getCollision(int layer)
        {
            if (this->collisions.find(layer) == this->collisions.end())
            {
                return CollisionType::NONE;
            }
            return this->collisions[layer];
        }

        void addCollision(CollisionType* collision, int layer)
        {
            this->collisions[layer] = *collision;
        }

        ~CollisionList()
        {
            this->collisions.clear();
        }
    };

    class CollisionMap
    {
        private:
        CollisionList* collisions;
        int length;

        public:
        CollisionMap()
        {
            this->collisions = new CollisionList[0];
            this->length = 0;
        }

        CollisionMap(int length)
        {
            this->collisions = new CollisionList[length];
            this->length = length;
        }

        CollisionMap(CollisionList* collisions, int length)
        {
            this->collisions = collisions;
            this->length = length;
        }

        /**
         * @brief Get the Collision Type
         * 
         * @param layer_start the layer to look for collisions
         * @param layer_end the layer that the layer_start is colliding with
         * @return CollisionType 
         */
        CollisionType getCollision(int layer_start, int layer_end)
        {
            if (this->length == 0)
            {
                return CollisionType::NONE;
            }

            if (layer_start >= this->length || layer_end >= this->length)
            {
                throw std::out_of_range("Layer out of range");
            }
            return this->collisions[layer_start].getCollision(layer_end);
        }

        ~CollisionMap()
        {
            // delete[] this->collisions;
        }

        /**
         * @brief Add a collision to a layer
         * 
         * @param collision 
         * @param layer_start the layer to add the collision to
         * @param layer_end the layer that the layer_start is colliding with
         */
        void addCollision(CollisionType* collision, int layer_start, int layer_end)
        {
            if (this->length == 0)
            {
                throw std::out_of_range("No layers defined at startup");
            }

            if (layer_start >= this->length || layer_start < 0)
            {
                throw std::out_of_range("Layer out of range");
            }
            this->collisions[layer_start].addCollision(collision, layer_end);
        }
    };
}