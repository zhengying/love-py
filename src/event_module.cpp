/**
 * Event module bindings
 */

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <SDL.h>

#include "love2d_common.h"

namespace py = pybind11;

void event_pump() {
    SDL_PumpEvents();
}

py::object event_poll() {
    SDL_Event e;
    if (SDL_PollEvent(&e)) {
        py::dict event;
        
        switch (e.type) {
            case SDL_QUIT:
                event["type"] = "quit";
                break;
                
            case SDL_KEYDOWN:
                event["type"] = "keypressed";
                event["key"] = SDL_GetKeyName(e.key.keysym.sym);
                event["scancode"] = e.key.keysym.scancode;
                event["isrepeat"] = e.key.repeat != 0;
                break;
                
            case SDL_KEYUP:
                event["type"] = "keyreleased";
                event["key"] = SDL_GetKeyName(e.key.keysym.sym);
                event["scancode"] = e.key.keysym.scancode;
                break;
                
            case SDL_MOUSEBUTTONDOWN:
                event["type"] = "mousepressed";
                event["x"] = e.button.x;
                event["y"] = e.button.y;
                event["button"] = e.button.button;
                event["istouch"] = e.button.which == SDL_TOUCH_MOUSEID;
                break;
                
            case SDL_MOUSEBUTTONUP:
                event["type"] = "mousereleased";
                event["x"] = e.button.x;
                event["y"] = e.button.y;
                event["button"] = e.button.button;
                event["istouch"] = e.button.which == SDL_TOUCH_MOUSEID;
                break;
                
            case SDL_MOUSEMOTION:
                event["type"] = "mousemoved";
                event["x"] = e.motion.x;
                event["y"] = e.motion.y;
                event["dx"] = e.motion.xrel;
                event["dy"] = e.motion.yrel;
                event["istouch"] = e.motion.which == SDL_TOUCH_MOUSEID;
                break;
                
            case SDL_WINDOWEVENT:
                if (e.window.event == SDL_WINDOWEVENT_RESIZED) {
                    event["type"] = "resize";
                    event["w"] = e.window.data1;
                    event["h"] = e.window.data2;
                } else if (e.window.event == SDL_WINDOWEVENT_FOCUS_GAINED) {
                    event["type"] = "focus";
                    event["focus"] = true;
                } else if (e.window.event == SDL_WINDOWEVENT_FOCUS_LOST) {
                    event["type"] = "focus";
                    event["focus"] = false;
                } else if (e.window.event == SDL_WINDOWEVENT_EXPOSED) {
                    event["type"] = "visible";
                    event["visible"] = true;
                } else if (e.window.event == SDL_WINDOWEVENT_HIDDEN) {
                    event["type"] = "visible";
                    event["visible"] = false;
                }
                break;
                
            default:
                event["type"] = "unknown";
                event["sdl_type"] = e.type;
                break;
        }
        
        return event;
    }
    
    return py::none();
}

void event_quit() {
    SDL_Event e;
    e.type = SDL_QUIT;
    SDL_PushEvent(&e);
}

void event_push(const std::string& event_type, py::kwargs kwargs) {
    SDL_Event e;
    
    if (event_type == "quit") {
        e.type = SDL_QUIT;
    } else {
        // Custom event type - simplified
        e.type = SDL_USEREVENT;
        e.user.code = 0;
    }
    
    SDL_PushEvent(&e);
}

void event_clear() {
    SDL_FlushEvents(SDL_FIRSTEVENT, SDL_LASTEVENT);
}

void init_event(py::module_ &m) {
    m.doc() = "Event handling functions";
    
    m.def("pump", &event_pump, "Poll for events from the OS");
    m.def("poll", &event_poll, "Get next event from the queue");
    m.def("quit", &event_quit, "Queue a quit event");
    m.def("push", &event_push, "Push an event to the queue",
          py::arg("event_type"));
    m.def("clear", &event_clear, "Clear the event queue");
}
