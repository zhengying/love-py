"""
Main API data containing all LÖVE 11.5 API definitions.
This file contains the complete API structure as Python dataclass instances.
"""
from .models import (
    LoveAPI, Module, Function, Type, Enum, EnumConstant,
    Variant, Argument, Return, Callback, TableField
)

# ============================================================================
# Global Functions (love.*)
# ============================================================================

LOVE_GET_VERSION = Function(
    name="getVersion",
    description="Gets the current running version of LÖVE.",
    variants=[
        Variant(
            description="For LÖVE versions below 0.9.1, the following variables can be used instead (and still work in 0.9.2 and newer):\\n\\nlove._version_major\\n\\nlove._version_minor\\n\\nlove._version_revision",
            returns=[
                Return(type="number", name="major", description="The major version of LÖVE, i.e. 0 for version 0.9.1."),
                Return(type="number", name="minor", description="The minor version of LÖVE, i.e. 9 for version 0.9.1."),
                Return(type="number", name="revision", description="The revision version of LÖVE, i.e. 1 for version 0.9.1."),
                Return(type="string", name="codename", description="The codename of the current version, i.e. 'Baby Inspector' for version 0.9.1."),
            ]
        )
    ]
)

LOVE_HAS_DEPRECATION_OUTPUT = Function(
    name="hasDeprecationOutput",
    description="Gets whether LÖVE displays warnings when using deprecated functionality. It is disabled by default in fused mode, and enabled by default otherwise.",
    variants=[
        Variant(
            returns=[
                Return(type="boolean", name="enabled", description="Whether deprecation output is enabled."),
            ]
        )
    ]
)

LOVE_IS_VERSION_COMPATIBLE = Function(
    name="isVersionCompatible",
    description="Gets whether the given version is compatible with the current running version of LÖVE.",
    variants=[
        Variant(
            arguments=[
                Argument(type="string", name="version", description="The version to check (for example '11.3' or '0.10.2')."),
            ],
            returns=[
                Return(type="boolean", name="compatible", description="Whether the given version is compatible with the current running version of LÖVE."),
            ]
        ),
        Variant(
            arguments=[
                Argument(type="number", name="major", description="The major version to check (for example 11 for 11.3 or 0 for 0.10.2)."),
                Argument(type="number", name="minor", description="The minor version to check (for example 3 for 11.3 or 10 for 0.10.2)."),
                Argument(type="number", name="revision", description="The revision of version to check (for example 0 for 11.3 or 2 for 0.10.2)."),
            ],
            returns=[
                Return(type="boolean", name="compatible", description="Whether the given version is compatible with the current running version of LÖVE."),
            ]
        )
    ]
)

LOVE_SET_DEPRECATION_OUTPUT = Function(
    name="setDeprecationOutput",
    description="Sets whether LÖVE displays warnings when using deprecated functionality.",
    variants=[
        Variant(
            arguments=[
                Argument(type="boolean", name="enable", description="Whether to enable or disable deprecation output."),
            ]
        )
    ]
)

# ============================================================================
# Callbacks
# ============================================================================

CALLBACK_CONF = Callback(
    name="conf",
    description="Called before LÖVE modules are loaded to configure the game.",
    variants=[
        Variant(
            arguments=[
                Argument(
                    type="table",
                    name="t",
                    description="Configuration table",
                    table=[
                        TableField(type="string", name="identity", description="Save directory name", default="nil"),
                        TableField(type="boolean", name="appendidentity", description="Search game dir before save dir", default="false"),
                        TableField(type="string", name="version", description="LÖVE version string", default='"11.5"'),
                        TableField(type="boolean", name="console", description="Open console (Windows only)", default="false"),
                    ]
                )
            ]
        )
    ]
)

CALLBACK_LOAD = Callback(
    name="load",
    description="Callback function triggered when the game is loaded.",
    variants=[
        Variant(
            arguments=[
                Argument(type="mixed", name="arg", description="Command line arguments", default="nil"),
            ]
        )
    ]
)

CALLBACK_UPDATE = Callback(
    name="update",
    description="Callback function triggered every frame to update the game state.",
    variants=[
        Variant(
            arguments=[
                Argument(type="number", name="dt", description="Time since the last update in seconds."),
            ]
        )
    ]
)

CALLBACK_DRAW = Callback(
    name="draw",
    description="Callback function triggered every frame to draw on the screen.",
    variants=[
        Variant()
    ]
)

CALLBACK_KEYPRESSED = Callback(
    name="keypressed",
    description="Callback function triggered when a key is pressed.",
    variants=[
        Variant(
            arguments=[
                Argument(type="KeyConstant", name="key", description="The key that was pressed."),
                Argument(type="Scancode", name="scancode", description="The scancode of the key."),
                Argument(type="boolean", name="isrepeat", description="Whether this keypress event is a repeat."),
            ]
        )
    ]
)

CALLBACK_KEYRELEASED = Callback(
    name="keyreleased",
    description="Callback function triggered when a key is released.",
    variants=[
        Variant(
            arguments=[
                Argument(type="KeyConstant", name="key", description="The key that was released."),
                Argument(type="Scancode", name="scancode", description="The scancode of the key."),
            ]
        )
    ]
)

CALLBACK_MOUSEPRESSED = Callback(
    name="mousepressed",
    description="Callback function triggered when a mouse button is pressed.",
    variants=[
        Variant(
            arguments=[
                Argument(type="number", name="x", description="Mouse x position."),
                Argument(type="number", name="y", description="Mouse y position."),
                Argument(type="number", name="button", description="The button index that was pressed."),
                Argument(type="boolean", name="istouch", description="Whether the press originated from a touch."),
                Argument(type="number", name="presses", description="The number of presses.", default="1"),
            ]
        )
    ]
)

CALLBACK_MOUSERELEASED = Callback(
    name="mousereleased",
    description="Callback function triggered when a mouse button is released.",
    variants=[
        Variant(
            arguments=[
                Argument(type="number", name="x", description="Mouse x position."),
                Argument(type="number", name="y", description="Mouse y position."),
                Argument(type="number", name="button", description="The button index that was released."),
                Argument(type="boolean", name="istouch", description="Whether the release originated from a touch."),
                Argument(type="number", name="presses", description="The number of presses.", default="1"),
            ]
        )
    ]
)

CALLBACK_MOUSEMOVED = Callback(
    name="mousemoved",
    description="Callback function triggered when the mouse is moved.",
    variants=[
        Variant(
            arguments=[
                Argument(type="number", name="x", description="Mouse x position."),
                Argument(type="number", name="y", description="Mouse y position."),
                Argument(type="number", name="dx", description="The amount moved along the x-axis since the last event."),
                Argument(type="number", name="dy", description="The amount moved along the y-axis since the last event."),
                Argument(type="boolean", name="istouch", description="Whether the move originated from a touch."),
            ]
        )
    ]
)

CALLBACK_JOYSTICKPRESSED = Callback(
    name="joystickpressed",
    description="Callback function triggered when a joystick button is pressed.",
    variants=[
        Variant(
            arguments=[
                Argument(type="Joystick", name="joystick", description="The joystick object."),
                Argument(type="number", name="button", description="The button index."),
            ]
        )
    ]
)

CALLBACK_JOYSTICKRELEASED = Callback(
    name="joystickreleased",
    description="Callback function triggered when a joystick button is released.",
    variants=[
        Variant(
            arguments=[
                Argument(type="Joystick", name="joystick", description="The joystick object."),
                Argument(type="number", name="button", description="The button index."),
            ]
        )
    ]
)

CALLBACK_FOCUS = Callback(
    name="focus",
    description="Callback function triggered when window receives or loses focus.",
    variants=[
        Variant(
            arguments=[
                Argument(type="boolean", name="focus", description="True if the window gains focus, false if it loses focus."),
            ]
        )
    ]
)

CALLBACK_QUIT = Callback(
    name="quit",
    description="Callback function triggered when the game is closed.",
    variants=[
        Variant(
            returns=[
                Return(type="boolean", name="prevent", description="Return true to prevent the game from exiting."),
            ]
        )
    ]
)

CALLBACK_RESIZE = Callback(
    name="resize",
    description="Called when the window is resized.",
    variants=[
        Variant(
            arguments=[
                Argument(type="number", name="w", description="The new width."),
                Argument(type="number", name="h", description="The new height."),
            ]
        )
    ]
)

CALLBACK_TOUCHPRESSED = Callback(
    name="touchpressed",
    description="Callback function triggered when a touch press moves inside the touch screen.",
    variants=[
        Variant(
            arguments=[
                Argument(type="light userdata", name="id", description="The identifier for the touch press."),
                Argument(type="number", name="x", description="The x-axis position of the touch press."),
                Argument(type="number", name="y", description="The y-axis position of the touch press."),
                Argument(type="number", name="dx", description="The x-axis movement of the touch press."),
                Argument(type="number", name="dy", description="The y-axis movement of the touch press."),
                Argument(type="number", name="pressure", description="The amount of pressure being used."),
            ]
        )
    ]
)

CALLBACK_TOUCHRELEASED = Callback(
    name="touchreleased",
    description="Callback function triggered when the touch screen stops being touched.",
    variants=[
        Variant(
            arguments=[
                Argument(type="light userdata", name="id", description="The identifier for the touch press."),
                Argument(type="number", name="x", description="The x-axis position of the touch press."),
                Argument(type="number", name="y", description="The y-axis position of the touch press."),
                Argument(type="number", name="dx", description="The x-axis movement of the touch press."),
                Argument(type="number", name="dy", description="The y-axis movement of the touch press."),
                Argument(type="number", name="pressure", description="The amount of pressure being used."),
            ]
        )
    ]
)

CALLBACK_TOUCHMOVED = Callback(
    name="touchmoved",
    description="Callback function triggered when a touch press moves inside the touch screen.",
    variants=[
        Variant(
            arguments=[
                Argument(type="light userdata", name="id", description="The identifier for the touch press."),
                Argument(type="number", name="x", description="The x-axis position of the touch press."),
                Argument(type="number", name="y", description="The y-axis position of the touch press."),
                Argument(type="number", name="dx", description="The x-axis movement of the touch press."),
                Argument(type="number", name="dy", description="The y-axis movement of the touch press."),
                Argument(type="number", name="pressure", description="The amount of pressure being used."),
            ]
        )
    ]
)

CALLBACK_WHEELMOVED = Callback(
    name="wheelmoved",
    description="Called when the mouse wheel is moved.",
    variants=[
        Variant(
            arguments=[
                Argument(type="number", name="x", description="Amount of horizontal mouse wheel movement. Positive values indicate movement to the right."),
                Argument(type="number", name="y", description="Amount of vertical mouse wheel movement. Positive values indicate upward movement."),
            ]
        )
    ]
)

CALLBACK_FILEDROPPED = Callback(
    name="filedropped",
    description="Called when a file is dragged and dropped onto the window.",
    variants=[
        Variant(
            arguments=[
                Argument(type="DroppedFile", name="file", description="The unopened File object representing the file that was dropped."),
            ]
        )
    ]
)

CALLBACK_DIRECTORYDROPPED = Callback(
    name="directorydropped",
    description="Called when a directory is dragged and dropped onto the window.",
    variants=[
        Variant(
            arguments=[
                Argument(type="string", name="path", description="The full platform-dependent path to the directory."),
            ]
        )
    ]
)

CALLBACK_JOYSTICKADDED = Callback(
    name="joystickadded",
    description="Called when a Joystick is connected.",
    variants=[
        Variant(
            arguments=[
                Argument(type="Joystick", name="joystick", description="The newly connected Joystick object."),
            ]
        )
    ]
)

CALLBACK_JOYSTICKREMOVED = Callback(
    name="joystickremoved",
    description="Called when a Joystick is disconnected.",
    variants=[
        Variant(
            arguments=[
                Argument(type="Joystick", name="joystick", description="The now-disconnected Joystick object."),
            ]
        )
    ]
)

CALLBACK_GAMEPADPRESSED = Callback(
    name="gamepadpressed",
    description="Called when a Joystick's virtual gamepad button is pressed.",
    variants=[
        Variant(
            arguments=[
                Argument(type="Joystick", name="joystick", description="The joystick object."),
                Argument(type="GamepadButton", name="button", description="The virtual gamepad button."),
            ]
        )
    ]
)

CALLBACK_GAMEPADRELEASED = Callback(
    name="gamepadreleased",
    description="Called when a Joystick's virtual gamepad button is released.",
    variants=[
        Variant(
            arguments=[
                Argument(type="Joystick", name="joystick", description="The joystick object."),
                Argument(type="GamepadButton", name="button", description="The virtual gamepad button."),
            ]
        )
    ]
)

CALLBACK_GAMEPADAXIS = Callback(
    name="gamepadaxis",
    description="Called when a Joystick's virtual gamepad axis is moved.",
    variants=[
        Variant(
            arguments=[
                Argument(type="Joystick", name="joystick", description="The joystick object."),
                Argument(type="GamepadAxis", name="axis", description="The virtual gamepad axis."),
                Argument(type="number", name="value", description="The new axis value."),
            ]
        )
    ]
)

CALLBACK_TEXTINPUT = Callback(
    name="textinput",
    description="Called when text is entered. For example pressing a key on the keyboard.",
    variants=[
        Variant(
            arguments=[
                Argument(type="string", name="text", description="The UTF-8 encoded unicode character."),
            ]
        )
    ]
)

CALLBACK_VISIBLE = Callback(
    name="visible",
    description="Callback function triggered when window is minimized/hidden or unminimized by the user.",
    variants=[
        Variant(
            arguments=[
                Argument(type="boolean", name="visible", description="True if the window is visible, false if it isn't."),
            ]
        )
    ]
)

# ============================================================================
# Module: Graphics
# ============================================================================

# Graphics Types
GRAPHICS_CANVAS_TYPE = Type(
    name="Canvas",
    description="Off-screen render target.",
    constructors=["newCanvas"],
    functions=[
        Function(
            name="renderTo",
            description="Render to the Canvas using a function.",
            variants=[
                Variant(
                    arguments=[
                        Argument(type="function", name="func", description="A function to render to the canvas."),
                    ]
                )
            ]
        ),
        Function(
            name="generateMipmaps",
            description="Generates mipmaps for the Canvas.",
            variants=[
                Variant()
            ]
        ),
    ],
    supertypes=["Texture", "Drawable", "Object"]
)

GRAPHICS_IMAGE_TYPE = Type(
    name="Image",
    description="Drawable image type.",
    constructors=["newImage"],
    functions=[
        Function(
            name="getWidth",
            description="Gets the width of the Image.",
            variants=[
                Variant(
                    returns=[
                        Return(type="number", name="width", description="The width of the Image, in pixels."),
                    ]
                )
            ]
        ),
        Function(
            name="getHeight",
            description="Gets the height of the Image.",
            variants=[
                Variant(
                    returns=[
                        Return(type="number", name="height", description="The height of the Image, in pixels."),
                    ]
                )
            ]
        ),
        Function(
            name="getDimensions",
            description="Gets the width and height of the Image.",
            variants=[
                Variant(
                    returns=[
                        Return(type="number", name="width", description="The width of the Image, in pixels."),
                        Return(type="number", name="height", description="The height of the Image, in pixels."),
                    ]
                )
            ]
        ),
        Function(
            name="getFilter",
            description="Gets the filter mode of the Image.",
            variants=[
                Variant(
                    returns=[
                        Return(type="FilterMode", name="min", description="Filter mode used when minimizing the image."),
                        Return(type="FilterMode", name="mag", description="Filter mode used when magnifying the image."),
                        Return(type="number", name="anisotropy", description="Maximum amount of Anisotropic Filtering used."),
                    ]
                )
            ]
        ),
        Function(
            name="setFilter",
            description="Sets the filter mode of the Image.",
            variants=[
                Variant(
                    arguments=[
                        Argument(type="FilterMode", name="min", description="Filter mode used when minimizing the image."),
                        Argument(type="FilterMode", name="mag", description="Filter mode used when magnifying the image.", default="min"),
                        Argument(type="number", name="anisotropy", description="Maximum amount of Anisotropic Filtering used.", default="1"),
                    ]
                )
            ]
        ),
        Function(
            name="getWrap",
            description="Gets the wrap mode of the Image.",
            variants=[
                Variant(
                    returns=[
                        Return(type="WrapMode", name="horiz", description="Horizontal wrapping mode."),
                        Return(type="WrapMode", name="vert", description="Vertical wrapping mode."),
                    ]
                )
            ]
        ),
        Function(
            name="setWrap",
            description="Sets the wrap mode of the Image.",
            variants=[
                Variant(
                    arguments=[
                        Argument(type="WrapMode", name="horiz", description="Horizontal wrapping mode."),
                        Argument(type="WrapMode", name="vert", description="Vertical wrapping mode.", default="horiz"),
                    ]
                )
            ]
        ),
        Function(
            name="replacePixels",
            description="Replace the contents of the Image.",
            variants=[
                Variant(
                    arguments=[
                        Argument(type="ImageData", name="data", description="The new ImageData to replace the contents with."),
                        Argument(type="number", name="x", description="The x-offset in pixels from the top-left of the image.", default="0"),
                        Argument(type="number", name="y", description="The y-offset in pixels from the top-left of the image.", default="0"),
                        Argument(type="boolean", name="reloadmipmaps", description="Whether to generate new mipmaps.", default="false"),
                    ]
                )
            ]
        ),
    ],
    supertypes=["Texture", "Drawable", "Object"]
)

GRAPHICS_FONT_TYPE = Type(
    name="Font",
    description="Defines the shape of characters that can be drawn onto the screen.",
    constructors=["newFont"],
    functions=[
        Function(
            name="getWidth",
            description="Gets the width of a string using the Font.",
            variants=[
                Variant(
                    arguments=[
                        Argument(type="string", name="text", description="The text to get the width of."),
                    ],
                    returns=[
                        Return(type="number", name="width", description="The width of the text."),
                    ]
                )
            ]
        ),
        Function(
            name="getHeight",
            description="Gets the height of the Font.",
            variants=[
                Variant(
                    returns=[
                        Return(type="number", name="height", description="The height of the Font, in pixels."),
                    ]
                )
            ]
        ),
        Function(
            name="getWrap",
            description="Gets the wrapping limit for the Font.",
            variants=[
                Variant(
                    arguments=[
                        Argument(type="string", name="text", description="The text to wrap."),
                        Argument(type="number", name="wrap", description="The maximum width in pixels."),
                    ],
                    returns=[
                        Return(type="number", name="width", description="The maximum width of the wrapped text."),
                        Return(type="table", name="wrappedtext", description="A table of strings, each being a line of text."),
                    ]
                )
            ]
        ),
        Function(
            name="setFilter",
            description="Sets the filter mode for the Font.",
            variants=[
                Variant(
                    arguments=[
                        Argument(type="FilterMode", name="min", description="Filter mode used when minimizing the font."),
                        Argument(type="FilterMode", name="mag", description="Filter mode used when magnifying the font.", default="min"),
                    ]
                )
            ]
        ),
        Function(
            name="getFilter",
            description="Gets the filter mode for the Font.",
            variants=[
                Variant(
                    returns=[
                        Return(type="FilterMode", name="min", description="The filter mode used when minimizing the font."),
                        Return(type="FilterMode", name="mag", description="The filter mode used when magnifying the font."),
                    ]
                )
            ]
        ),
        Function(
            name="getAscent",
            description="Gets the ascent of the Font.",
            variants=[
                Variant(
                    returns=[
                        Return(type="number", name="ascent", description="The ascent of the Font, in pixels."),
                    ]
                )
            ]
        ),
        Function(
            name="getDescent",
            description="Gets the descent of the Font.",
            variants=[
                Variant(
                    returns=[
                        Return(type="number", name="descent", description="The descent of the Font, in pixels."),
                    ]
                )
            ]
        ),
        Function(
            name="getBaseline",
            description="Gets the baseline of the Font.",
            variants=[
                Variant(
                    returns=[
                        Return(type="number", name="baseline", description="The baseline of the Font, in pixels."),
                    ]
                )
            ]
        ),
    ],
    supertypes=["Object"]
)

GRAPHICS_QUAD_TYPE = Type(
    name="Quad",
    description="Quadrilateral (a polygon with four sides and four corners) with texture coordinate information.",
    constructors=["newQuad"],
    functions=[
        Function(
            name="setViewport",
            description="Sets the texture coordinates of the Quad.",
            variants=[
                Variant(
                    arguments=[
                        Argument(type="number", name="x", description="The top-left corner x coordinate of the Quad."),
                        Argument(type="number", name="y", description="The top-left corner y coordinate of the Quad."),
                        Argument(type="number", name="w", description="The width of the Quad."),
                        Argument(type="number", name="h", description="The height of the Quad."),
                    ]
                )
            ]
        ),
        Function(
            name="getViewport",
            description="Gets the texture coordinates of the Quad.",
            variants=[
                Variant(
                    returns=[
                        Return(type="number", name="x", description="The top-left corner x coordinate of the Quad."),
                        Return(type="number", name="y", description="The top-left corner y coordinate of the Quad."),
                        Return(type="number", name="w", description="The width of the Quad."),
                        Return(type="number", name="h", description="The height of the Quad."),
                    ]
                )
            ]
        ),
        Function(
            name="getTextureDimensions",
            description="Gets the reference texture dimensions of the Quad.",
            variants=[
                Variant(
                    returns=[
                        Return(type="number", name="w", description="The width of the reference texture."),
                        Return(type="number", name="h", description="The height of the reference texture."),
                    ]
                )
            ]
        ),
    ],
    supertypes=["Object"]
)

GRAPHICS_SHADER_TYPE = Type(
    name="Shader",
    description="Shader object for custom vertex and fragment shaders.",
    constructors=["newShader"],
    functions=[
        Function(
            name="send",
            description="Sends one or more values to the shader.",
            variants=[
                Variant(
                    arguments=[
                        Argument(type="string", name="name", description="The name of the value to send to the shader."),
                        Argument(type="mixed", name="...", description="The values to send."),
                    ]
                )
            ]
        ),
        Function(
            name="sendColor",
            description="Sends one or more color values to the shader.",
            variants=[
                Variant(
                    arguments=[
                        Argument(type="string", name="name", description="The name of the color value to send."),
                        Argument(type="table", name="color", description="A table with red, green, blue, and alpha values."),
                    ]
                )
            ]
        ),
        Function(
            name="getWarnings",
            description="Gets any warnings that may have occurred during shader compilation.",
            variants=[
                Variant(
                    returns=[
                        Return(type="string", name="warnings", description="Shader compilation warnings."),
                    ]
                )
            ]
        ),
    ],
    supertypes=["Object"]
)

# Graphics Enums
DRAW_MODE_ENUM = Enum(
    name="DrawMode",
    description="How to draw arcs, ellipses, and rectangles.",
    constants=[
        EnumConstant(name="fill", description="Draw filled shape."),
        EnumConstant(name="line", description="Draw outlined shape."),
    ]
)

FILTER_MODE_ENUM = Enum(
    name="FilterMode",
    description="How to filter images when scaling.",
    constants=[
        EnumConstant(name="nearest", description="Use nearest neighbor interpolation."),
        EnumConstant(name="linear", description="Use linear interpolation."),
    ]
)

WRAP_MODE_ENUM = Enum(
    name="WrapMode",
    description="How to wrap textures.",
    constants=[
        EnumConstant(name="clamp", description="Clamp the texture."),
        EnumConstant(name="repeat", description="Repeat the texture."),
        EnumConstant(name="mirroredrepeat", description="Mirrored repeat the texture."),
    ]
)

BLEND_MODE_ENUM = Enum(
    name="BlendMode",
    description="How to blend colors.",
    constants=[
        EnumConstant(name="alpha", description="Alpha blending (normal)."),
        EnumConstant(name="replace", description="Replace mode (no blending)."),
        EnumConstant(name="add", description="Additive blending."),
        EnumConstant(name="subtract", description="Subtractive blending."),
        EnumConstant(name="multiply", description="Multiply blending."),
        EnumConstant(name="lighten", description="Lighten blending."),
        EnumConstant(name="darken", description="Darken blending."),
        EnumConstant(name="screen", description="Screen blending."),
    ]
)

ARC_TYPE_ENUM = Enum(
    name="ArcType",
    description="How to draw arcs.",
    constants=[
        EnumConstant(name="pie", description="Draw the arc like a pie."),
        EnumConstant(name="open", description="Draw the arc like an open curve."),
        EnumConstant(name="closed", description="Draw the arc like a closed curve."),
    ]
)

# Graphics Functions
GRAPHICS_NEW_IMAGE = Function(
    name="newImage",
    description="Creates a new Image from a file, FileData, or ImageData.",
    variants=[
        Variant(
            arguments=[
                Argument(type="string", name="filename", description="The filename of the image to load."),
                Argument(type="table", name="flags", description="Optional flags", default="nil"),
            ],
            returns=[
                Return(type="Image", name="image", description="The loaded image."),
            ]
        ),
        Variant(
            arguments=[
                Argument(type="FileData", name="filedata", description="The FileData to load from."),
                Argument(type="table", name="flags", description="Optional flags", default="nil"),
            ],
            returns=[
                Return(type="Image", name="image", description="The loaded image."),
            ]
        ),
        Variant(
            arguments=[
                Argument(type="ImageData", name="imagedata", description="The ImageData to load from."),
                Argument(type="table", name="flags", description="Optional flags", default="nil"),
            ],
            returns=[
                Return(type="Image", name="image", description="The loaded image."),
            ]
        ),
    ]
)

GRAPHICS_NEW_CANVAS = Function(
    name="newCanvas",
    description="Creates a new Canvas.",
    variants=[
        Variant(
            arguments=[
                Argument(type="number", name="width", description="The width of the canvas.", default="window width"),
                Argument(type="number", name="height", description="The height of the canvas.", default="window height"),
                Argument(type="table", name="settings", description="Canvas creation settings.", default="nil"),
            ],
            returns=[
                Return(type="Canvas", name="canvas", description="The created canvas."),
            ]
        )
    ]
)

GRAPHICS_NEW_FONT = Function(
    name="newFont",
    description="Creates a new Font.",
    variants=[
        Variant(
            arguments=[
                Argument(type="string", name="filename", description="The filename of the font to load."),
                Argument(type="number", name="size", description="The size of the font.", default="12"),
                Argument(type="table", name="hinting", description="True Type hinting mode.", default=""),
            ],
            returns=[
                Return(type="Font", name="font", description="The loaded font."),
            ]
        ),
        Variant(
            arguments=[
                Argument(type="number", name="size", description="The size of the default font.", default="12"),
            ],
            returns=[
                Return(type="Font", name="font", description="The default font."),
            ]
        ),
    ]
)

GRAPHICS_NEW_QUAD = Function(
    name="newQuad",
    description="Creates a new Quad.",
    variants=[
        Variant(
            arguments=[
                Argument(type="number", name="x", description="The top-left corner x coordinate."),
                Argument(type="number", name="y", description="The top-left corner y coordinate."),
                Argument(type="number", name="width", description="The width of the quad."),
                Argument(type="number", name="height", description="The height of the quad."),
                Argument(type="number", name="sw", description="The reference texture width."),
                Argument(type="number", name="sh", description="The reference texture height."),
            ],
            returns=[
                Return(type="Quad", name="quad", description="The created quad."),
            ]
        )
    ]
)

GRAPHICS_NEW_SHADER = Function(
    name="newShader",
    description="Creates a new Shader.",
    variants=[
        Variant(
            arguments=[
                Argument(type="string", name="code", description="The shader code."),
            ],
            returns=[
                Return(type="Shader", name="shader", description="The created shader."),
            ]
        ),
        Variant(
            arguments=[
                Argument(type="string", name="vertexcode", description="The vertex shader code."),
                Argument(type="string", name="pixelcode", description="The pixel shader code."),
            ],
            returns=[
                Return(type="Shader", name="shader", description="The created shader."),
            ]
        ),
    ]
)

GRAPHICS_DRAW = Function(
    name="draw",
    description="Draws a drawable object (Image, Canvas, etc.) to the screen.",
    variants=[
        Variant(
            arguments=[
                Argument(type="Drawable", name="drawable", description="The drawable object to draw."),
                Argument(type="number", name="x", description="The x-coordinate.", default="0"),
                Argument(type="number", name="y", description="The y-coordinate.", default="0"),
                Argument(type="number", name="r", description="The rotation (radians).", default="0"),
                Argument(type="number", name="sx", description="The x-axis scale.", default="1"),
                Argument(type="number", name="sy", description="The y-axis scale.", default="sx"),
                Argument(type="number", name="ox", description="The x-axis origin offset.", default="0"),
                Argument(type="number", name="oy", description="The y-axis origin offset.", default="0"),
                Argument(type="number", name="kx", description="The x-axis shear factor.", default="0"),
                Argument(type="number", name="ky", description="The y-axis shear factor.", default="0"),
            ]
        ),
        Variant(
            arguments=[
                Argument(type="Drawable", name="drawable", description="The drawable object to draw."),
                Argument(type="Quad", name="quad", description="The quad to draw."),
                Argument(type="number", name="x", description="The x-coordinate.", default="0"),
                Argument(type="number", name="y", description="The y-coordinate.", default="0"),
                Argument(type="number", name="r", description="The rotation (radians).", default="0"),
                Argument(type="number", name="sx", description="The x-axis scale.", default="1"),
                Argument(type="number", name="sy", description="The y-axis scale.", default="sx"),
                Argument(type="number", name="ox", description="The x-axis origin offset.", default="0"),
                Argument(type="number", name="oy", description="The y-axis origin offset.", default="0"),
                Argument(type="number", name="kx", description="The x-axis shear factor.", default="0"),
                Argument(type="number", name="ky", description="The y-axis shear factor.", default="0"),
            ]
        ),
    ]
)

GRAPHICS_RECTANGLE = Function(
    name="rectangle",
    description="Draws a rectangle.",
    variants=[
        Variant(
            arguments=[
                Argument(type="DrawMode", name="mode", description="How to draw the rectangle."),
                Argument(type="number", name="x", description="The x-coordinate."),
                Argument(type="number", name="y", description="The y-coordinate."),
                Argument(type="number", name="width", description="The width of the rectangle."),
                Argument(type="number", name="height", description="The height of the rectangle."),
            ]
        )
    ]
)

GRAPHICS_CIRCLE = Function(
    name="circle",
    description="Draws a circle.",
    variants=[
        Variant(
            arguments=[
                Argument(type="DrawMode", name="mode", description="How to draw the circle."),
                Argument(type="number", name="x", description="The x-coordinate."),
                Argument(type="number", name="y", description="The y-coordinate."),
                Argument(type="number", name="radius", description="The radius of the circle."),
            ]
        )
    ]
)

GRAPHICS_LINE = Function(
    name="line",
    description="Draws a line.",
    variants=[
        Variant(
            arguments=[
                Argument(type="number", name="x1", description="The x-coordinate of the first point."),
                Argument(type="number", name="y1", description="The y-coordinate of the first point."),
                Argument(type="number", name="x2", description="The x-coordinate of the second point."),
                Argument(type="number", name="y2", description="The y-coordinate of the second point."),
            ]
        ),
        Variant(
            arguments=[
                Argument(type="table", name="points", description="A table of points {x1, y1, x2, y2, ...}."),
            ]
        ),
    ]
)

GRAPHICS_PRINT = Function(
    name="print",
    description="Draws text on screen.",
    variants=[
        Variant(
            arguments=[
                Argument(type="string", name="text", description="The text to draw."),
                Argument(type="number", name="x", description="The x-coordinate.", default="0"),
                Argument(type="number", name="y", description="The y-coordinate.", default="0"),
                Argument(type="number", name="r", description="The rotation (radians).", default="0"),
                Argument(type="number", name="sx", description="The x-axis scale.", default="1"),
                Argument(type="number", name="sy", description="The y-axis scale.", default="sx"),
                Argument(type="number", name="ox", description="The x-axis origin offset.", default="0"),
                Argument(type="number", name="oy", description="The y-axis origin offset.", default="0"),
                Argument(type="number", name="kx", description="The x-axis shear factor.", default="0"),
                Argument(type="number", name="ky", description="The y-axis shear factor.", default="0"),
            ]
        ),
        Variant(
            arguments=[
                Argument(type="string", name="text", description="The text to draw."),
                Argument(type="Font", name="font", description="The font to use."),
                Argument(type="number", name="x", description="The x-coordinate.", default="0"),
                Argument(type="number", name="y", description="The y-coordinate.", default="0"),
                Argument(type="number", name="r", description="The rotation (radians).", default="0"),
                Argument(type="number", name="sx", description="The x-axis scale.", default="1"),
                Argument(type="number", name="sy", description="The y-axis scale.", default="sx"),
                Argument(type="number", name="ox", description="The x-axis origin offset.", default="0"),
                Argument(type="number", name="oy", description="The y-axis origin offset.", default="0"),
                Argument(type="number", name="kx", description="The x-axis shear factor.", default="0"),
                Argument(type="number", name="ky", description="The y-axis shear factor.", default="0"),
            ]
        ),
    ]
)

GRAPHICS_PRINTF = Function(
    name="printf",
    description="Draws formatted text with word wrapping.",
    variants=[
        Variant(
            arguments=[
                Argument(type="string", name="text", description="The text to draw."),
                Argument(type="number", name="x", description="The x-coordinate."),
                Argument(type="number", name="y", description="The y-coordinate."),
                Argument(type="number", name="limit", description="The wrap limit."),
                Argument(type="AlignMode", name="align", description="The alignment.", default="left"),
                Argument(type="number", name="r", description="The rotation (radians).", default="0"),
                Argument(type="number", name="sx", description="The x-axis scale.", default="1"),
                Argument(type="number", name="sy", description="The y-axis scale.", default="sx"),
                Argument(type="number", name="ox", description="The x-axis origin offset.", default="0"),
                Argument(type="number", name="oy", description="The y-axis origin offset.", default="0"),
                Argument(type="number", name="kx", description="The x-axis shear factor.", default="0"),
                Argument(type="number", name="ky", description="The y-axis shear factor.", default="0"),
            ]
        )
    ]
)

GRAPHICS_SET_COLOR = Function(
    name="setColor",
    description="Sets the color used for drawing.",
    variants=[
        Variant(
            arguments=[
                Argument(type="number", name="r", description="The red component (0-1)."),
                Argument(type="number", name="g", description="The green component (0-1)."),
                Argument(type="number", name="b", description="The blue component (0-1)."),
                Argument(type="number", name="a", description="The alpha component (0-1).", default="1"),
            ]
        ),
        Variant(
            arguments=[
                Argument(type="table", name="rgba", description="A table with r, g, b, and optional a components."),
            ]
        ),
    ]
)

GRAPHICS_GET_COLOR = Function(
    name="getColor",
    description="Gets the current color.",
    variants=[
        Variant(
            returns=[
                Return(type="number", name="r", description="The red component (0-1)."),
                Return(type="number", name="g", description="The green component (0-1)."),
                Return(type="number", name="b", description="The blue component (0-1)."),
                Return(type="number", name="a", description="The alpha component (0-1)."),
            ]
        )
    ]
)

GRAPHICS_SET_BACKGROUND_COLOR = Function(
    name="setBackgroundColor",
    description="Sets the background color.",
    variants=[
        Variant(
            arguments=[
                Argument(type="number", name="r", description="The red component (0-1)."),
                Argument(type="number", name="g", description="The green component (0-1)."),
                Argument(type="number", name="b", description="The blue component (0-1)."),
                Argument(type="number", name="a", description="The alpha component (0-1).", default="1"),
            ]
        ),
        Variant(
            arguments=[
                Argument(type="table", name="rgba", description="A table with r, g, b, and optional a components."),
            ]
        ),
    ]
)

GRAPHICS_GET_BACKGROUND_COLOR = Function(
    name="getBackgroundColor",
    description="Gets the background color.",
    variants=[
        Variant(
            returns=[
                Return(type="number", name="r", description="The red component (0-1)."),
                Return(type="number", name="g", description="The green component (0-1)."),
                Return(type="number", name="b", description="The blue component (0-1)."),
                Return(type="number", name="a", description="The alpha component (0-1)."),
            ]
        )
    ]
)

GRAPHICS_SET_BLEND_MODE = Function(
    name="setBlendMode",
    description="Sets the blend mode.",
    variants=[
        Variant(
            arguments=[
                Argument(type="BlendMode", name="mode", description="The blend mode."),
            ]
        )
    ]
)

GRAPHICS_GET_BLEND_MODE = Function(
    name="getBlendMode",
    description="Gets the blend mode.",
    variants=[
        Variant(
            returns=[
                Return(type="BlendMode", name="mode", description="The current blend mode."),
            ]
        )
    ]
)

GRAPHICS_PUSH = Function(
    name="push",
    description="Copies and pushes the current coordinate transformation to the transformation stack.",
    variants=[
        Variant(
            arguments=[
                Argument(type="StackType", name="stack", description="The stack to push to.", default="transform"),
            ]
        )
    ]
)

GRAPHICS_POP = Function(
    name="pop",
    description="Pops the current coordinate transformation from the transformation stack.",
    variants=[
        Variant(
            arguments=[
                Argument(type="StackType", name="stack", description="The stack to pop from.", default="transform"),
            ]
        )
    ]
)

GRAPHICS_TRANSLATE = Function(
    name="translate",
    description="Translates the coordinate system.",
    variants=[
        Variant(
            arguments=[
                Argument(type="number", name="dx", description="The translation along the x-axis."),
                Argument(type="number", name="dy", description="The translation along the y-axis."),
            ]
        )
    ]
)

GRAPHICS_ROTATE = Function(
    name="rotate",
    description="Rotates the coordinate system.",
    variants=[
        Variant(
            arguments=[
                Argument(type="number", name="angle", description="The rotation angle in radians."),
            ]
        )
    ]
)

GRAPHICS_SCALE = Function(
    name="scale",
    description="Scales the coordinate system.",
    variants=[
        Variant(
            arguments=[
                Argument(type="number", name="sx", description="The scaling along the x-axis."),
                Argument(type="number", name="sy", description="The scaling along the y-axis.", default="sx"),
            ]
        )
    ]
)

GRAPHICS_SHEAR = Function(
    name="shear",
    description="Shears the coordinate system.",
    variants=[
        Variant(
            arguments=[
                Argument(type="number", name="kx", description="The shearing along the x-axis."),
                Argument(type="number", name="ky", description="The shearing along the y-axis."),
            ]
        )
    ]
)

GRAPHICS_ORIGIN = Function(
    name="origin",
    description="Resets the transformation stack to the identity matrix.",
    variants=[
        Variant()
    ]
)

GRAPHICS_CLEAR = Function(
    name="clear",
    description="Clears the screen to the background color.",
    variants=[
        Variant(
            arguments=[
                Argument(type="table", name="color", description="Optional color to clear to.", default="nil"),
            ]
        ),
        Variant(
            arguments=[
                Argument(type="number", name="r", description="The red component."),
                Argument(type="number", name="g", description="The green component."),
                Argument(type="number", name="b", description="The blue component."),
                Argument(type="number", name="a", description="The alpha component.", default="1"),
            ]
        ),
    ]
)

GRAPHICS_PRESENT = Function(
    name="present",
    description="Displays the results of drawing operations on the screen.",
    variants=[
        Variant()
    ]
)

GRAPHICS_SET_CANVAS = Function(
    name="setCanvas",
    description="Sets the render target to a Canvas.",
    variants=[
        Variant(
            arguments=[
                Argument(type="Canvas", name="canvas", description="The Canvas to render to.", default="nil"),
            ]
        )
    ]
)

GRAPHICS_GET_CANVAS = Function(
    name="getCanvas",
    description="Gets the current render target Canvas.",
    variants=[
        Variant(
            returns=[
                Return(type="Canvas", name="canvas", description="The current Canvas, or nil."),
            ]
        )
    ]
)

GRAPHICS_SET_FONT = Function(
    name="setFont",
    description="Sets the font used for drawing text.",
    variants=[
        Variant(
            arguments=[
                Argument(type="Font", name="font", description="The font to use."),
            ]
        )
    ]
)

GRAPHICS_GET_FONT = Function(
    name="getFont",
    description="Gets the current font.",
    variants=[
        Variant(
            returns=[
                Return(type="Font", name="font", description="The current font."),
            ]
        )
    ]
)

GRAPHICS_SET_LINE_WIDTH = Function(
    name="setLineWidth",
    description="Sets the line width.",
    variants=[
        Variant(
            arguments=[
                Argument(type="number", name="width", description="The line width."),
            ]
        )
    ]
)

GRAPHICS_GET_LINE_WIDTH = Function(
    name="getLineWidth",
    description="Gets the line width.",
    variants=[
        Variant(
            returns=[
                Return(type="number", name="width", description="The current line width."),
            ]
        )
    ]
)

GRAPHICS_SET_POINT_SIZE = Function(
    name="setPointSize",
    description="Sets the point size.",
    variants=[
        Variant(
            arguments=[
                Argument(type="number", name="size", description="The point size."),
            ]
        )
    ]
)

GRAPHICS_GET_POINT_SIZE = Function(
    name="getPointSize",
    description="Gets the point size.",
    variants=[
        Variant(
            returns=[
                Return(type="number", name="size", description="The current point size."),
            ]
        )
    ]
)

GRAPHICS_SET_DEFAULT_FILTER = Function(
    name="setDefaultFilter",
    description="Sets the default filter mode for images.",
    variants=[
        Variant(
            arguments=[
                Argument(type="FilterMode", name="min", description="The filter mode used when downscaling."),
                Argument(type="FilterMode", name="mag", description="The filter mode used when upscaling.", default="min"),
                Argument(type="number", name="anisotropy", description="Maximum amount of anisotropic filtering.", default="1"),
            ]
        )
    ]
)

GRAPHICS_GET_DEFAULT_FILTER = Function(
    name="getDefaultFilter",
    description="Gets the default filter mode for images.",
    variants=[
        Variant(
            returns=[
                Return(type="FilterMode", name="min", description="The filter mode used when downscaling."),
                Return(type="FilterMode", name="mag", description="The filter mode used when upscaling."),
                Return(type="number", name="anisotropy", description="Maximum amount of anisotropic filtering."),
            ]
        )
    ]
)

GRAPHICS_GET_WIDTH = Function(
    name="getWidth",
    description="Gets the width of the window.",
    variants=[
        Variant(
            returns=[
                Return(type="number", name="width", description="The width of the window in pixels."),
            ]
        )
    ]
)

GRAPHICS_GET_HEIGHT = Function(
    name="getHeight",
    description="Gets the height of the window.",
    variants=[
        Variant(
            returns=[
                Return(type="number", name="height", description="The height of the window in pixels."),
            ]
        )
    ]
)

GRAPHICS_GET_DIMENSIONS = Function(
    name="getDimensions",
    description="Gets the dimensions of the window.",
    variants=[
        Variant(
            returns=[
                Return(type="number", name="width", description="The width of the window in pixels."),
                Return(type="number", name="height", description="The height of the window in pixels."),
            ]
        )
    ]
)

# Graphics Module
GRAPHICS_MODULE = Module(
    name="graphics",
    description="The primary responsibility for the love.graphics module is the drawing of lines, shapes, text, Images and other Drawable objects onto the screen.",
    types=[
        GRAPHICS_CANVAS_TYPE,
        GRAPHICS_IMAGE_TYPE,
        GRAPHICS_FONT_TYPE,
        GRAPHICS_QUAD_TYPE,
        GRAPHICS_SHADER_TYPE,
    ],
    functions=[
        GRAPHICS_NEW_IMAGE,
        GRAPHICS_NEW_CANVAS,
        GRAPHICS_NEW_FONT,
        GRAPHICS_NEW_QUAD,
        GRAPHICS_NEW_SHADER,
        GRAPHICS_DRAW,
        GRAPHICS_RECTANGLE,
        GRAPHICS_CIRCLE,
        GRAPHICS_LINE,
        GRAPHICS_PRINT,
        GRAPHICS_PRINTF,
        GRAPHICS_SET_COLOR,
        GRAPHICS_GET_COLOR,
        GRAPHICS_SET_BACKGROUND_COLOR,
        GRAPHICS_GET_BACKGROUND_COLOR,
        GRAPHICS_SET_BLEND_MODE,
        GRAPHICS_GET_BLEND_MODE,
        GRAPHICS_PUSH,
        GRAPHICS_POP,
        GRAPHICS_TRANSLATE,
        GRAPHICS_ROTATE,
        GRAPHICS_SCALE,
        GRAPHICS_SHEAR,
        GRAPHICS_ORIGIN,
        GRAPHICS_CLEAR,
        GRAPHICS_PRESENT,
        GRAPHICS_SET_CANVAS,
        GRAPHICS_GET_CANVAS,
        GRAPHICS_SET_FONT,
        GRAPHICS_GET_FONT,
        GRAPHICS_SET_LINE_WIDTH,
        GRAPHICS_GET_LINE_WIDTH,
        GRAPHICS_SET_POINT_SIZE,
        GRAPHICS_GET_POINT_SIZE,
        GRAPHICS_SET_DEFAULT_FILTER,
        GRAPHICS_GET_DEFAULT_FILTER,
        GRAPHICS_GET_WIDTH,
        GRAPHICS_GET_HEIGHT,
        GRAPHICS_GET_DIMENSIONS,
    ],
    enums=[
        DRAW_MODE_ENUM,
        FILTER_MODE_ENUM,
        WRAP_MODE_ENUM,
        BLEND_MODE_ENUM,
        ARC_TYPE_ENUM,
    ]
)

# ============================================================================
# Module: Keyboard
# ============================================================================

# Keyboard Functions
KEYBOARD_IS_DOWN = Function(
    name="isDown",
    description="Checks whether a certain key is pressed.",
    variants=[
        Variant(
            arguments=[
                Argument(type="KeyConstant", name="key", description="The key to check."),
            ],
            returns=[
                Return(type="boolean", name="down", description="True if the key is down, false otherwise."),
            ]
        ),
        Variant(
            arguments=[
                Argument(type="KeyConstant", name="...", description="Multiple keys to check."),
            ],
            returns=[
                Return(type="boolean", name="anyDown", description="True if any of the keys are down."),
            ]
        ),
    ]
)

KEYBOARD_IS_SCANCODE_DOWN = Function(
    name="isScancodeDown",
    description="Checks whether the specified Scancodes are pressed.",
    variants=[
        Variant(
            arguments=[
                Argument(type="Scancode", name="...", description="The Scancodes to check."),
            ],
            returns=[
                Return(type="boolean", name="down", description="True if any of the scancodes are down."),
            ]
        )
    ]
)

KEYBOARD_SET_KEY_REPEAT = Function(
    name="setKeyRepeat",
    description="Enables or disables key repeat.",
    variants=[
        Variant(
            arguments=[
                Argument(type="boolean", name="enable", description="Whether key repeat should be enabled."),
            ]
        )
    ]
)

KEYBOARD_HAS_KEY_REPEAT = Function(
    name="hasKeyRepeat",
    description="Gets whether key repeat is enabled.",
    variants=[
        Variant(
            returns=[
                Return(type="boolean", name="enabled", description="True if key repeat is enabled."),
            ]
        )
    ]
)

KEYBOARD_SET_TEXT_INPUT = Function(
    name="setTextInput",
    description="Enables or disables text input events.",
    variants=[
        Variant(
            arguments=[
                Argument(type="boolean", name="enable", description="Whether text input events should be enabled."),
            ]
        ),
        Variant(
            arguments=[
                Argument(type="boolean", name="enable", description="Whether text input events should be enabled."),
                Argument(type="number", name="x", description="The on-screen x coordinate of the text input field."),
                Argument(type="number", name="y", description="The on-screen y coordinate of the text input field."),
                Argument(type="number", name="w", description="The width of the text input field."),
                Argument(type="number", name="h", description="The height of the text input field."),
            ]
        ),
    ]
)

KEYBOARD_HAS_SCREEN_KEYBOARD = Function(
    name="hasScreenKeyboard",
    description="Gets whether the platform has a screen keyboard available.",
    variants=[
        Variant(
            returns=[
                Return(type="boolean", name="enabled", description="True if the platform has a screen keyboard."),
            ]
        )
    ]
)

KEYBOARD_HAS_TEXT_INPUT = Function(
    name="hasTextInput",
    description="Gets whether text input events are enabled.",
    variants=[
        Variant(
            returns=[
                Return(type="boolean", name="enabled", description="True if text input events are enabled."),
            ]
        )
    ]
)

# Keyboard Enums
KEY_CONSTANT_ENUM = Enum(
    name="KeyConstant",
    description="Keyboard key constants.",
    constants=[
        EnumConstant(name="a", description="The A key."),
        EnumConstant(name="b", description="The B key."),
        EnumConstant(name="c", description="The C key."),
        EnumConstant(name="d", description="The D key."),
        EnumConstant(name="e", description="The E key."),
        EnumConstant(name="f", description="The F key."),
        EnumConstant(name="g", description="The G key."),
        EnumConstant(name="h", description="The H key."),
        EnumConstant(name="i", description="The I key."),
        EnumConstant(name="j", description="The J key."),
        EnumConstant(name="k", description="The K key."),
        EnumConstant(name="l", description="The L key."),
        EnumConstant(name="m", description="The M key."),
        EnumConstant(name="n", description="The N key."),
        EnumConstant(name="o", description="The O key."),
        EnumConstant(name="p", description="The P key."),
        EnumConstant(name="q", description="The Q key."),
        EnumConstant(name="r", description="The R key."),
        EnumConstant(name="s", description="The S key."),
        EnumConstant(name="t", description="The T key."),
        EnumConstant(name="u", description="The U key."),
        EnumConstant(name="v", description="The V key."),
        EnumConstant(name="w", description="The W key."),
        EnumConstant(name="x", description="The X key."),
        EnumConstant(name="y", description="The Y key."),
        EnumConstant(name="z", description="The Z key."),
        EnumConstant(name="0", description="The 0 key."),
        EnumConstant(name="1", description="The 1 key."),
        EnumConstant(name="2", description="The 2 key."),
        EnumConstant(name="3", description="The 3 key."),
        EnumConstant(name="4", description="The 4 key."),
        EnumConstant(name="5", description="The 5 key."),
        EnumConstant(name="6", description="The 6 key."),
        EnumConstant(name="7", description="The 7 key."),
        EnumConstant(name="8", description="The 8 key."),
        EnumConstant(name="9", description="The 9 key."),
        EnumConstant(name="space", description="The Space key."),
        EnumConstant(name="return", description="The Return/Enter key."),
        EnumConstant(name="escape", description="The Escape key."),
        EnumConstant(name="tab", description="The Tab key."),
        EnumConstant(name="left", description="The Left arrow key."),
        EnumConstant(name="right", description="The Right arrow key."),
        EnumConstant(name="up", description="The Up arrow key."),
        EnumConstant(name="down", description="The Down arrow key."),
        EnumConstant(name="lshift", description="The Left Shift key."),
        EnumConstant(name="rshift", description="The Right Shift key."),
        EnumConstant(name="lctrl", description="The Left Control key."),
        EnumConstant(name="rctrl", description="The Right Control key."),
        EnumConstant(name="lalt", description="The Left Alt key."),
        EnumConstant(name="ralt", description="The Right Alt key."),
        EnumConstant(name="lgui", description="The Left GUI/Command/Windows key."),
        EnumConstant(name="rgui", description="The Right GUI/Command/Windows key."),
        EnumConstant(name="backspace", description="The Backspace key."),
        EnumConstant(name="delete", description="The Delete key."),
        EnumConstant(name="insert", description="The Insert key."),
        EnumConstant(name="home", description="The Home key."),
        EnumConstant(name="end", description="The End key."),
        EnumConstant(name="pageup", description="The Page Up key."),
        EnumConstant(name="pagedown", description="The Page Down key."),
        EnumConstant(name="f1", description="The F1 key."),
        EnumConstant(name="f2", description="The F2 key."),
        EnumConstant(name="f3", description="The F3 key."),
        EnumConstant(name="f4", description="The F4 key."),
        EnumConstant(name="f5", description="The F5 key."),
        EnumConstant(name="f6", description="The F6 key."),
        EnumConstant(name="f7", description="The F7 key."),
        EnumConstant(name="f8", description="The F8 key."),
        EnumConstant(name="f9", description="The F9 key."),
        EnumConstant(name="f10", description="The F10 key."),
        EnumConstant(name="f11", description="The F11 key."),
        EnumConstant(name="f12", description="The F12 key."),
    ]
)

# Keyboard Module
KEYBOARD_MODULE = Module(
    name="keyboard",
    description="Provides an interface to the user's keyboard.",
    types=[],
    functions=[
        KEYBOARD_IS_DOWN,
        KEYBOARD_IS_SCANCODE_DOWN,
        KEYBOARD_SET_KEY_REPEAT,
        KEYBOARD_HAS_KEY_REPEAT,
        KEYBOARD_SET_TEXT_INPUT,
        KEYBOARD_HAS_SCREEN_KEYBOARD,
        KEYBOARD_HAS_TEXT_INPUT,
    ],
    enums=[
        KEY_CONSTANT_ENUM,
    ]
)

# ============================================================================
# Module: Mouse
# ============================================================================

# Mouse Functions
MOUSE_GET_POSITION = Function(
    name="getPosition",
    description="Gets the current position of the mouse.",
    variants=[
        Variant(
            returns=[
                Return(type="number", name="x", description="The x position of the mouse."),
                Return(type="number", name="y", description="The y position of the mouse."),
            ]
        )
    ]
)

MOUSE_GET_X = Function(
    name="getX",
    description="Gets the current x position of the mouse.",
    variants=[
        Variant(
            returns=[
                Return(type="number", name="x", description="The x position of the mouse."),
            ]
        )
    ]
)

MOUSE_GET_Y = Function(
    name="getY",
    description="Gets the current y position of the mouse.",
    variants=[
        Variant(
            returns=[
                Return(type="number", name="y", description="The y position of the mouse."),
            ]
        )
    ]
)

MOUSE_IS_DOWN = Function(
    name="isDown",
    description="Checks whether a mouse button is down.",
    variants=[
        Variant(
            arguments=[
                Argument(type="number", name="button", description="The button index (1, 2, or 3)."),
            ],
            returns=[
                Return(type="boolean", name="down", description="True if the button is down."),
            ]
        ),
        Variant(
            arguments=[
                Argument(type="number", name="...", description="Multiple button indices."),
            ],
            returns=[
                Return(type="boolean", name="anyDown", description="True if any of the buttons are down."),
            ]
        ),
    ]
)

MOUSE_SET_POSITION = Function(
    name="setPosition",
    description="Sets the position of the mouse.",
    variants=[
        Variant(
            arguments=[
                Argument(type="number", name="x", description="The x position."),
                Argument(type="number", name="y", description="The y position."),
            ]
        )
    ]
)

MOUSE_SET_VISIBLE = Function(
    name="setVisible",
    description="Sets whether the cursor is visible.",
    variants=[
        Variant(
            arguments=[
                Argument(type="boolean", name="visible", description="Whether the cursor should be visible."),
            ]
        )
    ]
)

MOUSE_IS_VISIBLE = Function(
    name="isVisible",
    description="Gets whether the cursor is visible.",
    variants=[
        Variant(
            returns=[
                Return(type="boolean", name="visible", description="True if the cursor is visible."),
            ]
        )
    ]
)

MOUSE_SET_GRABBED = Function(
    name="setGrabbed",
    description="Sets whether the cursor is confined to the window.",
    variants=[
        Variant(
            arguments=[
                Argument(type="boolean", name="grabbed", description="Whether the cursor should be grabbed."),
            ]
        )
    ]
)

MOUSE_IS_GRABBED = Function(
    name="isGrabbed",
    description="Gets whether the cursor is confined to the window.",
    variants=[
        Variant(
            returns=[
                Return(type="boolean", name="grabbed", description="True if the cursor is grabbed."),
            ]
        )
    ]
)

MOUSE_SET_RELATIVE_MODE = Function(
    name="setRelativeMode",
    description="Sets whether the mouse is in relative mode.",
    variants=[
        Variant(
            arguments=[
                Argument(type="boolean", name="enable", description="Whether relative mode should be enabled."),
            ]
        )
    ]
)

# Mouse Module
MOUSE_MODULE = Module(
    name="mouse",
    description="Provides an interface to the user's mouse.",
    types=[],
    functions=[
        MOUSE_GET_POSITION,
        MOUSE_GET_X,
        MOUSE_GET_Y,
        MOUSE_IS_DOWN,
        MOUSE_SET_POSITION,
        MOUSE_SET_VISIBLE,
        MOUSE_IS_VISIBLE,
        MOUSE_SET_GRABBED,
        MOUSE_IS_GRABBED,
        MOUSE_SET_RELATIVE_MODE,
    ],
    enums=[]
)

# ============================================================================
# Module: Timer
# ============================================================================

TIMER_GET_TIME = Function(
    name="getTime",
    description="Gets the current running time.",
    variants=[
        Variant(
            returns=[
                Return(type="number", name="time", description="The current time in seconds."),
            ]
        )
    ]
)

TIMER_GET_DELTA = Function(
    name="getDelta",
    description="Gets the time between frames.",
    variants=[
        Variant(
            returns=[
                Return(type="number", name="dt", description="The time between frames in seconds."),
            ]
        )
    ]
)

TIMER_GET_FPS = Function(
    name="getFPS",
    description="Gets the current frames per second.",
    variants=[
        Variant(
            returns=[
                Return(type="number", name="fps", description="The current FPS."),
            ]
        )
    ]
)

TIMER_SLEEP = Function(
    name="sleep",
    description="Sleeps the program for the specified amount of time.",
    variants=[
        Variant(
            arguments=[
                Argument(type="number", name="s", description="The time to sleep in seconds."),
            ]
        )
    ]
)

TIMER_MODULE = Module(
    name="timer",
    description="Provides high-resolution timing functionality.",
    types=[],
    functions=[
        TIMER_GET_TIME,
        TIMER_GET_DELTA,
        TIMER_GET_FPS,
        TIMER_SLEEP,
    ],
    enums=[]
)

# ============================================================================
# Module: Window
# ============================================================================

WINDOW_SET_MODE = Function(
    name="setMode",
    description="Sets the window mode.",
    variants=[
        Variant(
            arguments=[
                Argument(type="number", name="width", description="The window width."),
                Argument(type="number", name="height", description="The window height."),
                Argument(type="table", name="flags", description="Window flags.", default="nil"),
            ],
            returns=[
                Return(type="boolean", name="success", description="True if successful."),
            ]
        )
    ]
)

WINDOW_GET_MODE = Function(
    name="getMode",
    description="Gets the window mode.",
    variants=[
        Variant(
            returns=[
                Return(type="number", name="width", description="The window width."),
                Return(type="number", name="height", description="The window height."),
                Return(type="table", name="flags", description="The window flags."),
            ]
        )
    ]
)

WINDOW_SET_TITLE = Function(
    name="setTitle",
    description="Sets the window title.",
    variants=[
        Variant(
            arguments=[
                Argument(type="string", name="title", description="The new window title."),
            ]
        )
    ]
)

WINDOW_GET_TITLE = Function(
    name="getTitle",
    description="Gets the window title.",
    variants=[
        Variant(
            returns=[
                Return(type="string", name="title", description="The current window title."),
            ]
        )
    ]
)

WINDOW_SET_ICON = Function(
    name="setIcon",
    description="Sets the window icon.",
    variants=[
        Variant(
            arguments=[
                Argument(type="ImageData", name="imagedata", description="The icon image data."),
            ],
            returns=[
                Return(type="boolean", name="success", description="True if successful."),
            ]
        )
    ]
)

WINDOW_SET_POSITION = Function(
    name="setPosition",
    description="Sets the window position.",
    variants=[
        Variant(
            arguments=[
                Argument(type="number", name="x", description="The x-coordinate."),
                Argument(type="number", name="y", description="The y-coordinate."),
                Argument(type="number", name="display", description="The display index.", default="1"),
            ]
        )
    ]
)

WINDOW_GET_POSITION = Function(
    name="getPosition",
    description="Gets the window position.",
    variants=[
        Variant(
            returns=[
                Return(type="number", name="x", description="The x-coordinate."),
                Return(type="number", name="y", description="The y-coordinate."),
                Return(type="number", name="display", description="The display index."),
            ]
        )
    ]
)

WINDOW_SET_FULLSCREEN = Function(
    name="setFullscreen",
    description="Sets fullscreen mode.",
    variants=[
        Variant(
            arguments=[
                Argument(type="boolean", name="fullscreen", description="Whether to enable fullscreen."),
                Argument(type="FullscreenType", name="fstype", description="The type of fullscreen to use.", default="exclusive"),
            ],
            returns=[
                Return(type="boolean", name="success", description="True if successful."),
            ]
        )
    ]
)

WINDOW_GET_FULLSCREEN = Function(
    name="getFullscreen",
    description="Gets fullscreen mode.",
    variants=[
        Variant(
            returns=[
                Return(type="boolean", name="fullscreen", description="True if in fullscreen mode."),
                Return(type="FullscreenType", name="fstype", description="The type of fullscreen."),
            ]
        )
    ]
)

WINDOW_SET_VSYNC = Function(
    name="setVSync",
    description="Sets vertical sync mode.",
    variants=[
        Variant(
            arguments=[
                Argument(type="boolean", name="vsync", description="Whether to enable vsync."),
            ]
        )
    ]
)

WINDOW_GET_VSYNC = Function(
    name="getVSync",
    description="Gets vertical sync mode.",
    variants=[
        Variant(
            returns=[
                Return(type="boolean", name="vsync", description="True if vsync is enabled."),
            ]
        )
    ]
)

WINDOW_SHOW_MESSAGE_BOX = Function(
    name="showMessageBox",
    description="Displays a message box.",
    variants=[
        Variant(
            arguments=[
                Argument(type="string", name="title", description="The title of the message box."),
                Argument(type="string", name="message", description="The message text."),
                Argument(type="MessageBoxType", name="type", description="The type of message box.", default="info"),
                Argument(type="boolean", name="attachToWindow", description="Whether to attach to the window.", default="true"),
            ],
            returns=[
                Return(type="boolean", name="success", description="True if successful."),
            ]
        ),
        Variant(
            arguments=[
                Argument(type="string", name="title", description="The title of the message box."),
                Argument(type="string", name="message", description="The message text."),
                Argument(type="table", name="buttons", description="A table of button names."),
                Argument(type="number", name="enterbutton", description="The index of the enter button.", default="1"),
                Argument(type="number", name="escapebutton", description="The index of the escape button.", default="0"),
                Argument(type="boolean", name="attachToWindow", description="Whether to attach to the window.", default="true"),
            ],
            returns=[
                Return(type="number", name="buttonindex", description="The index of the button pressed."),
            ]
        ),
    ]
)

WINDOW_CLOSE = Function(
    name="close",
    description="Closes the window.",
    variants=[
        Variant()
    ]
)

WINDOW_MODULE = Module(
    name="window",
    description="Provides an interface for the program's window.",
    types=[],
    functions=[
        WINDOW_SET_MODE,
        WINDOW_GET_MODE,
        WINDOW_SET_TITLE,
        WINDOW_GET_TITLE,
        WINDOW_SET_ICON,
        WINDOW_SET_POSITION,
        WINDOW_GET_POSITION,
        WINDOW_SET_FULLSCREEN,
        WINDOW_GET_FULLSCREEN,
        WINDOW_SET_VSYNC,
        WINDOW_GET_VSYNC,
        WINDOW_SHOW_MESSAGE_BOX,
        WINDOW_CLOSE,
    ],
    enums=[]
)

# ============================================================================
# Module: Event
# ============================================================================

EVENT_PUMP = Function(
    name="pump",
    description="Pumps events into the event queue.",
    variants=[
        Variant()
    ]
)

EVENT_POLL = Function(
    name="poll",
    description="Gets an event from the queue.",
    variants=[
        Variant(
            returns=[
                Return(type="string", name="name", description="The event name, or nil if no events."),
                Return(type="mixed", name="...", description="The event arguments."),
            ]
        )
    ]
)

EVENT_WAIT = Function(
    name="wait",
    description="Waits for and returns the next event.",
    variants=[
        Variant(
            returns=[
                Return(type="string", name="name", description="The event name."),
                Return(type="mixed", name="...", description="The event arguments."),
            ]
        )
    ]
)

EVENT_CLEAR = Function(
    name="clear",
    description="Clears the event queue.",
    variants=[
        Variant()
    ]
)

EVENT_MODULE = Module(
    name="event",
    description="Manages events like key presses.",
    types=[],
    functions=[
        EVENT_PUMP,
        EVENT_POLL,
        EVENT_WAIT,
        EVENT_CLEAR,
    ],
    enums=[]
)

# ============================================================================
# Module: Filesystem
# ============================================================================

FILESYSTEM_READ = Function(
    name="read",
    description="Reads the contents of a file.",
    variants=[
        Variant(
            arguments=[
                Argument(type="string", name="name", description="The name (and path) of the file."),
                Argument(type="number", name="bytes", description="The number of bytes to read.", default="all"),
            ],
            returns=[
                Return(type="string", name="contents", description="The file contents, or nil on failure."),
                Return(type="number", name="size", description="The size of the file in bytes."),
            ]
        )
    ]
)

FILESYSTEM_WRITE = Function(
    name="write",
    description="Writes data to a file.",
    variants=[
        Variant(
            arguments=[
                Argument(type="string", name="name", description="The name (and path) of the file."),
                Argument(type="string", name="data", description="The data to write."),
            ],
            returns=[
                Return(type="boolean", name="success", description="True if successful."),
                Return(type="string", name="errormsg", description="The error message on failure."),
            ]
        ),
        Variant(
            arguments=[
                Argument(type="string", name="name", description="The name (and path) of the file."),
                Argument(type="string", name="data", description="The data to write."),
                Argument(type="number", name="bytes", description="The number of bytes to write."),
            ],
            returns=[
                Return(type="boolean", name="success", description="True if successful."),
                Return(type="string", name="errormsg", description="The error message on failure."),
            ]
        ),
    ]
)

FILESYSTEM_APPEND = Function(
    name="append",
    description="Appends data to a file.",
    variants=[
        Variant(
            arguments=[
                Argument(type="string", name="name", description="The name (and path) of the file."),
                Argument(type="string", name="data", description="The data to append."),
            ],
            returns=[
                Return(type="boolean", name="success", description="True if successful."),
                Return(type="string", name="errormsg", description="The error message on failure."),
            ]
        ),
        Variant(
            arguments=[
                Argument(type="string", name="name", description="The name (and path) of the file."),
                Argument(type="string", name="data", description="The data to append."),
                Argument(type="number", name="bytes", description="The number of bytes to append."),
            ],
            returns=[
                Return(type="boolean", name="success", description="True if successful."),
                Return(type="string", name="errormsg", description="The error message on failure."),
            ]
        ),
    ]
)

FILESYSTEM_EXISTS = Function(
    name="exists",
    description="Checks if a file or directory exists.",
    variants=[
        Variant(
            arguments=[
                Argument(type="string", name="path", description="The path to check."),
            ],
            returns=[
                Return(type="boolean", name="exists", description="True if the file/directory exists."),
            ]
        )
    ]
)

FILESYSTEM_GET_INFO = Function(
    name="getInfo",
    description="Gets information about a file or directory.",
    variants=[
        Variant(
            arguments=[
                Argument(type="string", name="path", description="The path to check."),
                Argument(type="FileType", name="filtertype", description="If supplied, filters by type.", default="nil"),
            ],
            returns=[
                Return(type="table", name="info", description="A table with file information, or nil."),
            ]
        )
    ]
)

FILESYSTEM_GET_SIZE = Function(
    name="getSize",
    description="Gets the size of a file.",
    variants=[
        Variant(
            arguments=[
                Argument(type="string", name="filename", description="The filename to check."),
            ],
            returns=[
                Return(type="number", name="size", description="The file size in bytes, or nil."),
            ]
        )
    ]
)

FILESYSTEM_IS_FILE = Function(
    name="isFile",
    description="Checks if something is a file.",
    variants=[
        Variant(
            arguments=[
                Argument(type="string", name="path", description="The path to check."),
            ],
            returns=[
                Return(type="boolean", name="isfile", description="True if the path is a file."),
            ]
        )
    ]
)

FILESYSTEM_IS_DIRECTORY = Function(
    name="isDirectory",
    description="Checks if something is a directory.",
    variants=[
        Variant(
            arguments=[
                Argument(type="string", name="path", description="The path to check."),
            ],
            returns=[
                Return(type="boolean", name="isdir", description="True if the path is a directory."),
            ]
        )
    ]
)

FILESYSTEM_CREATE_DIRECTORY = Function(
    name="createDirectory",
    description="Creates a directory.",
    variants=[
        Variant(
            arguments=[
                Argument(type="string", name="name", description="The name of the directory to create."),
            ],
            returns=[
                Return(type="boolean", name="success", description="True if successful."),
            ]
        )
    ]
)

FILESYSTEM_GET_DIRECTORY_ITEMS = Function(
    name="getDirectoryItems",
    description="Gets the items in a directory.",
    variants=[
        Variant(
            arguments=[
                Argument(type="string", name="dir", description="The directory to list."),
            ],
            returns=[
                Return(type="table", name="items", description="A table of item names."),
            ]
        )
    ]
)

FILESYSTEM_SET_IDENTITY = Function(
    name="setIdentity",
    description="Sets the write directory.",
    variants=[
        Variant(
            arguments=[
                Argument(type="string", name="name", description="The identity name."),
                Argument(type="boolean", name="append", description="Whether to search the game directory first.", default="false"),
            ]
        )
    ]
)

FILESYSTEM_GET_IDENTITY = Function(
    name="getIdentity",
    description="Gets the write directory.",
    variants=[
        Variant(
            returns=[
                Return(type="string", name="name", description="The identity name."),
            ]
        )
    ]
)

FILESYSTEM_GET_APPDATA_DIRECTORY = Function(
    name="getAppdataDirectory",
    description="Gets the appdata directory.",
    variants=[
        Variant(
            returns=[
                Return(type="string", name="path", description="The appdata directory path."),
            ]
        )
    ]
)

FILESYSTEM_GET_SAVE_DIRECTORY = Function(
    name="getSaveDirectory",
    description="Gets the save directory.",
    variants=[
        Variant(
            returns=[
                Return(type="string", name="path", description="The save directory path."),
            ]
        )
    ]
)

FILESYSTEM_GET_SOURCE = Function(
    name="getSource",
    description="Returns the full path to the the .love file or directory.",
    variants=[
        Variant(
            returns=[
                Return(type="string", name="path", description="The full platform-dependent path of the .love file or directory."),
            ]
        )
    ]
)

FILESYSTEM_GET_SOURCE_BASE_DIRECTORY = Function(
    name="getSourceBaseDirectory",
    description="Returns the full path to the directory containing the .love file.",
    variants=[
        Variant(
            returns=[
                Return(type="string", name="path", description="The base directory of the current game."),
            ]
        )
    ]
)

FILESYSTEM_GET_WORKING_DIRECTORY = Function(
    name="getWorkingDirectory",
    description="Gets the working directory.",
    variants=[
        Variant(
            returns=[
                Return(type="string", name="path", description="The current working directory."),
            ]
        )
    ]
)

FILESYSTEM_MODULE = Module(
    name="filesystem",
    description="Provides an interface to the user's filesystem.",
    types=[],
    functions=[
        FILESYSTEM_READ,
        FILESYSTEM_WRITE,
        FILESYSTEM_APPEND,
        FILESYSTEM_EXISTS,
        FILESYSTEM_GET_INFO,
        FILESYSTEM_GET_SIZE,
        FILESYSTEM_IS_FILE,
        FILESYSTEM_IS_DIRECTORY,
        FILESYSTEM_CREATE_DIRECTORY,
        FILESYSTEM_GET_DIRECTORY_ITEMS,
        FILESYSTEM_SET_IDENTITY,
        FILESYSTEM_GET_IDENTITY,
        FILESYSTEM_GET_APPDATA_DIRECTORY,
        FILESYSTEM_GET_SAVE_DIRECTORY,
        FILESYSTEM_GET_SOURCE,
        FILESYSTEM_GET_SOURCE_BASE_DIRECTORY,
        FILESYSTEM_GET_WORKING_DIRECTORY,
    ],
    enums=[]
)

# ============================================================================
# Module: Audio
# ============================================================================

AUDIO_NEW_SOURCE = Function(
    name="newSource",
    description="Creates a new audio Source.",
    variants=[
        Variant(
            arguments=[
                Argument(type="string", name="filename", description="The filename of the audio to load."),
                Argument(type="SourceType", name="type", description="The type of source to create.", default="static"),
            ],
            returns=[
                Return(type="Source", name="source", description="The new Source."),
            ]
        ),
        Variant(
            arguments=[
                Argument(type="File", name="file", description="A File to load the audio from."),
                Argument(type="SourceType", name="type", description="The type of source to create.", default="static"),
            ],
            returns=[
                Return(type="Source", name="source", description="The new Source."),
            ]
        ),
        Variant(
            arguments=[
                Argument(type="SoundData", name="sounddata", description="SoundData to create Source from."),
            ],
            returns=[
                Return(type="Source", name="source", description="The new Source."),
            ]
        ),
    ]
)

AUDIO_PLAY = Function(
    name="play",
    description="Plays a Source.",
    variants=[
        Variant(
            arguments=[
                Argument(type="Source", name="source", description="The Source to play."),
            ]
        )
    ]
)

AUDIO_STOP = Function(
    name="stop",
    description="Stops a Source.",
    variants=[
        Variant(
            arguments=[
                Argument(type="Source", name="source", description="The Source to stop.", default="nil"),
            ]
        )
    ]
)

AUDIO_PAUSE = Function(
    name="pause",
    description="Pauses a Source.",
    variants=[
        Variant(
            arguments=[
                Argument(type="Source", name="source", description="The Source to pause.", default="nil"),
            ]
        )
    ]
)

AUDIO_RESUME = Function(
    name="resume",
    description="Resumes a Source.",
    variants=[
        Variant(
            arguments=[
                Argument(type="Source", name="source", description="The Source to resume.", default="nil"),
            ]
        )
    ]
)

AUDIO_REWIND = Function(
    name="rewind",
    description="Rewinds a Source.",
    variants=[
        Variant(
            arguments=[
                Argument(type="Source", name="source", description="The Source to rewind.", default="nil"),
            ]
        )
    ]
)

AUDIO_SET_VOLUME = Function(
    name="setVolume",
    description="Sets the master volume.",
    variants=[
        Variant(
            arguments=[
                Argument(type="number", name="volume", description="The master volume (0.0 to 1.0)."),
            ]
        )
    ]
)

AUDIO_GET_VOLUME = Function(
    name="getVolume",
    description="Gets the master volume.",
    variants=[
        Variant(
            returns=[
                Return(type="number", name="volume", description="The current master volume."),
            ]
        )
    ]
)

AUDIO_SET_POSITION = Function(
    name="setPosition",
    description="Sets the position of the listener.",
    variants=[
        Variant(
            arguments=[
                Argument(type="number", name="x", description="The x position."),
                Argument(type="number", name="y", description="The y position."),
                Argument(type="number", name="z", description="The z position.", default="0"),
            ]
        )
    ]
)

AUDIO_GET_POSITION = Function(
    name="getPosition",
    description="Gets the position of the listener.",
    variants=[
        Variant(
            returns=[
                Return(type="number", name="x", description="The x position."),
                Return(type="number", name="y", description="The y position."),
                Return(type="number", name="z", description="The z position."),
            ]
        )
    ]
)

AUDIO_MODULE = Module(
    name="audio",
    description="Provides an interface to output audio to the user's speakers.",
    types=[],
    functions=[
        AUDIO_NEW_SOURCE,
        AUDIO_PLAY,
        AUDIO_STOP,
        AUDIO_PAUSE,
        AUDIO_RESUME,
        AUDIO_REWIND,
        AUDIO_SET_VOLUME,
        AUDIO_GET_VOLUME,
        AUDIO_SET_POSITION,
        AUDIO_GET_POSITION,
    ],
    enums=[]
)

# ============================================================================
# Module: Math
# ============================================================================

MATH_NEW_RANDOM_GENERATOR = Function(
    name="newRandomGenerator",
    description="Creates a new RandomGenerator object.",
    variants=[
        Variant(
            arguments=[
                Argument(type="number", name="seed", description="The seed number.", default="os.time()"),
            ],
            returns=[
                Return(type="RandomGenerator", name="generator", description="The new RandomGenerator."),
            ]
        ),
        Variant(
            arguments=[
                Argument(type="number", name="low", description="The low 32 bits of the seed number."),
                Argument(type="number", name="high", description="The high 32 bits of the seed number."),
            ],
            returns=[
                Return(type="RandomGenerator", name="generator", description="The new RandomGenerator."),
            ]
        ),
    ]
)

MATH_RANDOM = Function(
    name="random",
    description="Generates a random number.",
    variants=[
        Variant(
            returns=[
                Return(type="number", name="number", description="A random number between 0 and 1."),
            ]
        ),
        Variant(
            arguments=[
                Argument(type="number", name="m", description="The upper limit."),
            ],
            returns=[
                Return(type="number", name="number", description="A random integer between 1 and m."),
            ]
        ),
        Variant(
            arguments=[
                Argument(type="number", name="m", description="The lower limit."),
                Argument(type="number", name="n", description="The upper limit."),
            ],
            returns=[
                Return(type="number", name="number", description="A random integer between m and n."),
            ]
        ),
    ]
)

MATH_RANDOM_SEED = Function(
    name="randomSeed",
    description="Sets the seed of the random number generator.",
    variants=[
        Variant(
            arguments=[
                Argument(type="number", name="seed", description="The new seed."),
            ]
        ),
        Variant(
            arguments=[
                Argument(type="number", name="low", description="The low 32 bits of the seed."),
                Argument(type="number", name="high", description="The high 32 bits of the seed."),
            ]
        ),
    ]
)

MATH_SET_RANDOM_SEED = Function(
    name="setRandomSeed",
    description="Sets the seed of the random number generator.",
    variants=[
        Variant(
            arguments=[
                Argument(type="number", name="seed", description="The new seed."),
            ]
        ),
        Variant(
            arguments=[
                Argument(type="number", name="low", description="The low 32 bits of the seed."),
                Argument(type="number", name="high", description="The high 32 bits of the seed."),
            ]
        ),
    ]
)

MATH_GET_RANDOM_SEED = Function(
    name="getRandomSeed",
    description="Gets the seed of the random number generator.",
    variants=[
        Variant(
            returns=[
                Return(type="number", name="low", description="The low 32 bits of the seed."),
                Return(type="number", name="high", description="The high 32 bits of the seed."),
            ]
        )
    ]
)

MATH_NEW_TRANSFORM = Function(
    name="newTransform",
    description="Creates a new Transform.",
    variants=[
        Variant(
            returns=[
                Return(type="Transform", name="transform", description="The new Transform."),
            ]
        ),
        Variant(
            arguments=[
                Argument(type="number", name="x", description="The x translation."),
                Argument(type="number", name="y", description="The y translation."),
                Argument(type="number", name="rotation", description="The rotation.", default="0"),
                Argument(type="number", name="sx", description="The x scaling.", default="1"),
                Argument(type="number", name="sy", description="The y scaling.", default="sx"),
                Argument(type="number", name="ox", description="The x origin offset.", default="0"),
                Argument(type="number", name="oy", description="The y origin offset.", default="0"),
                Argument(type="number", name="kx", description="The x shearing.", default="0"),
                Argument(type="number", name="ky", description="The y shearing.", default="0"),
            ],
            returns=[
                Return(type="Transform", name="transform", description="The new Transform."),
            ]
        ),
    ]
)

MATH_NEW_BEZIER_CURVE = Function(
    name="newBezierCurve",
    description="Creates a new BezierCurve.",
    variants=[
        Variant(
            arguments=[
                Argument(type="table", name="points", description="A table of control points."),
            ],
            returns=[
                Return(type="BezierCurve", name="curve", description="The new BezierCurve."),
            ]
        )
    ]
)

MATH_GAMMA_TO_LINEAR = Function(
    name="gammaToLinear",
    description="Converts from gamma-space to linear-space.",
    variants=[
        Variant(
            arguments=[
                Argument(type="number", name="c", description="The gamma-space component."),
            ],
            returns=[
                Return(type="number", name="l", description="The linear-space component."),
            ]
        ),
        Variant(
            arguments=[
                Argument(type="number", name="r", description="The gamma-space red component."),
                Argument(type="number", name="g", description="The gamma-space green component."),
                Argument(type="number", name="b", description="The gamma-space blue component."),
            ],
            returns=[
                Return(type="number", name="lr", description="The linear-space red component."),
                Return(type="number", name="lg", description="The linear-space green component."),
                Return(type="number", name="lb", description="The linear-space blue component."),
            ]
        ),
    ]
)

MATH_LINEAR_TO_GAMMA = Function(
    name="linearToGamma",
    description="Converts from linear-space to gamma-space.",
    variants=[
        Variant(
            arguments=[
                Argument(type="number", name="c", description="The linear-space component."),
            ],
            returns=[
                Return(type="number", name="g", description="The gamma-space component."),
            ]
        ),
        Variant(
            arguments=[
                Argument(type="number", name="lr", description="The linear-space red component."),
                Argument(type="number", name="lg", description="The linear-space green component."),
                Argument(type="number", name="lb", description="The linear-space blue component."),
            ],
            returns=[
                Return(type="number", name="r", description="The gamma-space red component."),
                Return(type="number", name="g", description="The gamma-space green component."),
                Return(type="number", name="b", description="The gamma-space blue component."),
            ]
        ),
    ]
)

MATH_IS_CONVEX = Function(
    name="isConvex",
    description="Checks whether a polygon is convex.",
    variants=[
        Variant(
            arguments=[
                Argument(type="table", name="vertices", description="The vertices of the polygon."),
            ],
            returns=[
                Return(type="boolean", name="convex", description="True if the polygon is convex."),
            ]
        )
    ]
)

MATH_TRIANGULATE = Function(
    name="triangulate",
    description="Triangulates a polygon.",
    variants=[
        Variant(
            arguments=[
                Argument(type="table", name="vertices", description="The vertices of the polygon."),
            ],
            returns=[
                Return(type="table", name="triangles", description="A table of triangles."),
            ]
        )
    ]
)

MATH_MODULE = Module(
    name="math",
    description="Provides system-independent mathematical functions.",
    types=[],
    functions=[
        MATH_NEW_RANDOM_GENERATOR,
        MATH_RANDOM,
        MATH_RANDOM_SEED,
        MATH_SET_RANDOM_SEED,
        MATH_GET_RANDOM_SEED,
        MATH_NEW_TRANSFORM,
        MATH_NEW_BEZIER_CURVE,
        MATH_GAMMA_TO_LINEAR,
        MATH_LINEAR_TO_GAMMA,
        MATH_IS_CONVEX,
        MATH_TRIANGULATE,
    ],
    enums=[]
)

# ============================================================================
# Module: Touch
# ============================================================================

TOUCH_GET_TOUCHES = Function(
    name="getTouches",
    description="Gets all currently active touches.",
    variants=[
        Variant(
            returns=[
                Return(type="table", name="touches", description="A table of active touch identifiers."),
            ]
        )
    ]
)

TOUCH_GET_POSITION = Function(
    name="getPosition",
    description="Gets the position of a touch.",
    variants=[
        Variant(
            arguments=[
                Argument(type="light userdata", name="id", description="The touch identifier."),
            ],
            returns=[
                Return(type="number", name="x", description="The x position."),
                Return(type="number", name="y", description="The y position."),
            ]
        )
    ]
)

TOUCH_GET_PRESSURE = Function(
    name="getPressure",
    description="Gets the pressure of a touch.",
    variants=[
        Variant(
            arguments=[
                Argument(type="light userdata", name="id", description="The touch identifier."),
            ],
            returns=[
                Return(type="number", name="pressure", description="The touch pressure."),
            ]
        )
    ]
)

TOUCH_MODULE = Module(
    name="touch",
    description="Provides an interface to touch-screen presses.",
    types=[],
    functions=[
        TOUCH_GET_TOUCHES,
        TOUCH_GET_POSITION,
        TOUCH_GET_PRESSURE,
    ],
    enums=[]
)

# ============================================================================
# Main API
# ============================================================================

API = LoveAPI(
    version="11.5",
    functions=[
        LOVE_GET_VERSION,
        LOVE_HAS_DEPRECATION_OUTPUT,
        LOVE_IS_VERSION_COMPATIBLE,
        LOVE_SET_DEPRECATION_OUTPUT,
    ],
    modules=[
        GRAPHICS_MODULE,
        KEYBOARD_MODULE,
        MOUSE_MODULE,
        TIMER_MODULE,
        WINDOW_MODULE,
        EVENT_MODULE,
        FILESYSTEM_MODULE,
        AUDIO_MODULE,
        MATH_MODULE,
        TOUCH_MODULE,
    ],
    types=[],  # Global types
    callbacks=[
        CALLBACK_CONF,
        CALLBACK_LOAD,
        CALLBACK_UPDATE,
        CALLBACK_DRAW,
        CALLBACK_KEYPRESSED,
        CALLBACK_KEYRELEASED,
        CALLBACK_MOUSEPRESSED,
        CALLBACK_MOUSERELEASED,
        CALLBACK_MOUSEMOVED,
        CALLBACK_JOYSTICKPRESSED,
        CALLBACK_JOYSTICKRELEASED,
        CALLBACK_FOCUS,
        CALLBACK_QUIT,
        CALLBACK_RESIZE,
        CALLBACK_TOUCHPRESSED,
        CALLBACK_TOUCHRELEASED,
        CALLBACK_TOUCHMOVED,
        CALLBACK_WHEELMOVED,
        CALLBACK_FILEDROPPED,
        CALLBACK_DIRECTORYDROPPED,
        CALLBACK_JOYSTICKADDED,
        CALLBACK_JOYSTICKREMOVED,
        CALLBACK_GAMEPADPRESSED,
        CALLBACK_GAMEPADRELEASED,
        CALLBACK_GAMEPADAXIS,
        CALLBACK_TEXTINPUT,
        CALLBACK_VISIBLE,
    ]
)
