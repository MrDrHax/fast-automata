#include <pybind11/pybind11.h>
#include <pybind11/functional.h>  
#include <pybind11/stl.h>         
#include "ClassTypes.hpp"
#include "Board.hpp"
#include "Agents.hpp"

namespace py = pybind11;

using namespace fastautomata::Board;
using namespace fastautomata::ClassTypes;
using namespace fastautomata::Agents;

PYBIND11_MODULE(fastautomata_clib, m) {
    py::class_<SimulatedBoard>(m, "SimulatedBoard")
        .def(py::init<int, int, int>())
        .def("getWidth", &SimulatedBoard::getWidth)
        .def("getHeight", &SimulatedBoard::getHeight)
        .def("getLayerCount", &SimulatedBoard::getLayerCount)
        .def("reset", &SimulatedBoard::reset)
        .def("step", &SimulatedBoard::step)
        .def("agent_get", &SimulatedBoard::agent_get)
        .def("agent_add", &SimulatedBoard::agent_add)
        .def("agent_remove", &SimulatedBoard::agent_remove)
        .def("agent_move", &SimulatedBoard::agent_move)
        .def("agent_move_layer", &SimulatedBoard::agent_move_layer)
        .def("update_agents", &SimulatedBoard::update_agents)
        .def("update_agents_end", &SimulatedBoard::update_agents_end)
        .def("getCollisions", &SimulatedBoard::getCollisions)
        .def("getRandomColor", &SimulatedBoard::getRandomColor)
        .def("updateColor", &SimulatedBoard::updateColor)
        .def("addColor", &SimulatedBoard::addColor)
        .def("append_on_add", &SimulatedBoard::append_on_add)
        .def("append_on_delete", &SimulatedBoard::append_on_delete)
        .def("append_on_reset", &SimulatedBoard::append_on_reset)
        .def("step_instructions_add", &SimulatedBoard::step_instructions_add)
        .def("step_instructions_flush", &SimulatedBoard::step_instructions_flush)
        .def_readonly("color_map_count", &SimulatedBoard::color_map_count)
        .def_readwrite("layer_collisions", &SimulatedBoard::layer_collisions)
        .def_readwrite("step_instructions", &SimulatedBoard::step_instructions)
        .def_readwrite("color_map", &SimulatedBoard::color_map)
        .def_readwrite("on_reset", &SimulatedBoard::on_reset)
        .def_readwrite("on_add", &SimulatedBoard::on_add)
        .def_readwrite("on_delete", &SimulatedBoard::on_delete)
        .def_readwrite("python_on_delete", &SimulatedBoard::python_on_delete);

    py::class_<BaseAgent, BaseAgentPy>(m, "BaseAgent")
        .def(py::init<>(), py::return_value_policy::take_ownership)
        .def(py::init<SimulatedBoard*, Pos, std::string, int, bool>(), py::return_value_policy::take_ownership)
        .def_property("pos",
            py::cpp_function(&BaseAgent::getPos, py::return_value_policy::copy),
            py::cpp_function())
        .def("getId", &BaseAgent::getId)
        .def("getLayer", &BaseAgent::getLayer)
        .def_property("state", &BaseAgent::getState, py::cpp_function())
        .def("kill", &BaseAgent::kill)
        .def_readonly("board", &BaseAgent::board)
        .def("checkCollisions", &BaseAgent::checkCollisions);

    py::class_<Agent, BaseAgent, PyAgent>(m, "Agent")
        .def(py::init<>(), py::return_value_policy::take_ownership)
        .def(py::init<fastautomata::Board::SimulatedBoard*, fastautomata::ClassTypes::Pos, std::string, int, bool>(), py::return_value_policy::take_ownership)
        .def("step", &Agent::step)
        .def("step_end", &Agent::step_end)
        .def_property("pos",
            py::cpp_function(&Agent::getPos, py::return_value_policy::copy),
            py::cpp_function(&Agent::setPos))
        .def_property("state", &Agent::getState, &Agent::setState)
        .def("get_neighbors", &Agent::get_neighbors)
        .def_readwrite("on_update", &Agent::on_update)
        .def("append_on_update", &Agent::append_on_update)
        .def("__repr__", &Agent::toString)
        .def("__str__", &Agent::objInfo);
        
    py::class_<Pos>(m, "Pos")
        .def(py::init<>())
        .def(py::init<int, int>())
        .def("copy", &Pos::copy)
        .def("toIndex", &Pos::toIndex)
        .def("magnitude", &Pos::magnitude)
        .def("normalize", &Pos::normalize)
        .def("toString", &Pos::toString)
        .def("__eq__", &Pos::operator==)
        .def("__ne__", &Pos::operator!=)
        .def("__gt__", &Pos::operator>)
        .def("__lt__", &Pos::operator<)
        .def("__repr__", &Pos::toString)
        .def("__str__", &Pos::toString)
        .def("__hash__", &Pos::toIndex)
        .def("__add__", &Pos::operator+)
        .def("__sub__", &Pos::operator-)
        .def("__mul__", &Pos::operator*)
        .def("__div__", &Pos::operator/)
        .def("__floordiv__", &Pos::operator/)
        .def("__mod__", &Pos::operator%)
        .def("__iadd__", &Pos::operator+=)
        .def("__isub__", &Pos::operator-=)
        .def("__imul__", &Pos::operator*=)
        .def("__idiv__", &Pos::operator/=)
        .def("__ifloordiv__", &Pos::operator/=)
        .def("__imod__", &Pos::operator%=)
        .def_readwrite("x", &Pos::x)
        .def_readwrite("y", &Pos::y);

    py::enum_<CollisionType>(m, "CollisionType")
        .value("NONE", CollisionType::NONE)
        .value("SOLID", CollisionType::SOLID)
        .value("TRIGGER", CollisionType::TRIGGER)
        .export_values();

    py::class_<CollisionList>(m, "CollisionList")
        .def(py::init<>())
        .def("getCollision", &CollisionList::getCollision)
        .def("addCollision", &CollisionList::addCollision);

    py::class_<CollisionMap>(m, "CollisionMap")
        .def(py::init<>())
        .def(py::init<int>())
        .def(py::init<CollisionList*, int>())
        .def("getCollision", &CollisionMap::getCollision)
        .def("addCollision", &CollisionMap::addCollision);

}