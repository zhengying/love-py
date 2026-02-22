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

GRAPHICS_MESH_TYPE = Type(
    name="Mesh",
    description="Mesh object.",
    constructors=["newMesh"],
    functions=[
        Function(name="setVertices", description="Method setVertices.", variants=[]),
        Function(name="getVertices", description="Method getVertices.", variants=[]),
        Function(name="setVertexMap", description="Method setVertexMap.", variants=[]),
        Function(name="flush", description="Method flush.", variants=[]),
    ],
    supertypes=["Object"]
)

GRAPHICS_SPRITE_BATCH_TYPE = Type(
    name="SpriteBatch",
    description="SpriteBatch object.",
    constructors=["newSpriteBatch"],
    functions=[
        Function(name="add", description="Method add.", variants=[]),
        Function(name="set", description="Method set.", variants=[]),
        Function(name="clear", description="Method clear.", variants=[]),
        Function(name="flush", description="Method flush.", variants=[]),
        Function(name="getCount", description="Method getCount.", variants=[]),
        Function(name="getBufferSize", description="Method getBufferSize.", variants=[]),
    ],
    supertypes=["Object"]
)

GRAPHICS_PARTICLE_SYSTEM_TYPE = Type(
    name="ParticleSystem",
    description="ParticleSystem object.",
    constructors=["newParticleSystem"],
    functions=[
        Function(name="emit", description="Method emit.", variants=[]),
        Function(name="update", description="Method update.", variants=[]),
        Function(name="start", description="Method start.", variants=[]),
        Function(name="stop", description="Method stop.", variants=[]),
        Function(name="reset", description="Method reset.", variants=[]),
        Function(name="isActive", description="Method isActive.", variants=[]),
        Function(name="getCount", description="Method getCount.", variants=[]),
        Function(name="setTexture", description="Method setTexture.", variants=[]),
    ],
    supertypes=["Object"]
)

GRAPHICS_TEXT_TYPE = Type(
    name="Text",
    description="Drawable text object.",
    constructors=["newText"],
    functions=[
        Function(name="set", description="Method set.", variants=[]),
        Function(name="add", description="Method add.", variants=[]),
        Function(name="clear", description="Method clear.", variants=[]),
        Function(name="getWidth", description="Method getWidth.", variants=[]),
        Function(name="getHeight", description="Method getHeight.", variants=[]),
    ],
    supertypes=["Object"]
)

GRAPHICS_VIDEO_TYPE = Type(
    name="Video",
    description="Video object.",
    constructors=["newVideo"],
    functions=[
        Function(name="play", description="Method play.", variants=[]),
        Function(name="pause", description="Method pause.", variants=[]),
        Function(name="seek", description="Method seek.", variants=[]),
        Function(name="tell", description="Method tell.", variants=[]),
        Function(name="isPlaying", description="Method isPlaying.", variants=[]),
        Function(name="getWidth", description="Method getWidth.", variants=[]),
        Function(name="getHeight", description="Method getHeight.", variants=[]),
        Function(name="getSource", description="Method getSource.", variants=[]),
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

GRAPHICS_ALIGN_MODE_ENUM = Enum(
    name="AlignMode",
    description="AlignMode constants.",
    constants=[
        EnumConstant(name="left", description=""),
        EnumConstant(name="center", description=""),
        EnumConstant(name="right", description=""),
        EnumConstant(name="justify", description=""),
    ]
)

GRAPHICS_BLEND_ALPHA_MODE_ENUM = Enum(
    name="BlendAlphaMode",
    description="BlendAlphaMode constants.",
    constants=[
        EnumConstant(name="alphamultiply", description=""),
        EnumConstant(name="premultiplied", description=""),
    ]
)

GRAPHICS_LINE_STYLE_ENUM = Enum(
    name="LineStyle",
    description="LineStyle constants.",
    constants=[
        EnumConstant(name="smooth", description=""),
        EnumConstant(name="rough", description=""),
    ]
)

GRAPHICS_LINE_JOIN_ENUM = Enum(
    name="LineJoin",
    description="LineJoin constants.",
    constants=[
        EnumConstant(name="none", description=""),
        EnumConstant(name="miter", description=""),
        EnumConstant(name="bevel", description=""),
    ]
)

GRAPHICS_STACK_TYPE_ENUM = Enum(
    name="StackType",
    description="StackType constants.",
    constants=[
        EnumConstant(name="transform", description=""),
        EnumConstant(name="all", description=""),
    ]
)

GRAPHICS_MESH_DRAW_MODE_ENUM = Enum(
    name="MeshDrawMode",
    description="MeshDrawMode constants.",
    constants=[
        EnumConstant(name="fan", description=""),
        EnumConstant(name="strip", description=""),
        EnumConstant(name="triangles", description=""),
        EnumConstant(name="points", description=""),
    ]
)

GRAPHICS_COMPARE_MODE_ENUM = Enum(
    name="CompareMode",
    description="CompareMode constants.",
    constants=[
        EnumConstant(name="equal", description=""),
        EnumConstant(name="notequal", description=""),
        EnumConstant(name="less", description=""),
        EnumConstant(name="lequal", description=""),
        EnumConstant(name="gequal", description=""),
        EnumConstant(name="greater", description=""),
        EnumConstant(name="always", description=""),
        EnumConstant(name="never", description=""),
    ]
)

GRAPHICS_CULL_MODE_ENUM = Enum(
    name="CullMode",
    description="CullMode constants.",
    constants=[
        EnumConstant(name="none", description=""),
        EnumConstant(name="back", description=""),
        EnumConstant(name="front", description=""),
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

GRAPHICS_NEW_IMAGE_FONT = Function(
    name="newImageFont",
    description="Creates a new Font from an image and a string of glyphs.",
    variants=[
        Variant(
            arguments=[
                Argument(type="Image", name="image", description="The image containing the glyphs."),
                Argument(type="string", name="glyphs", description="The string of glyphs in the image."),
            ],
            returns=[
                Return(type="Font", name="font", description="The created font."),
            ]
        )
    ]
)

GRAPHICS_NEW_TEXT = Function(
    name="newText",
    description="Creates a new drawable Text object.",
    variants=[
        Variant(
            arguments=[
                Argument(type="Font", name="font", description="The font to use."),
                Argument(type="string", name="text", description="The initial text.", default=""),
            ],
            returns=[
                Return(type="Text", name="text", description="The created Text object."),
            ]
        ),
        Variant(
            arguments=[
                Argument(type="Font", name="font", description="The font to use."),
            ],
            returns=[
                Return(type="Text", name="text", description="The created Text object."),
            ]
        ),
    ]
)

GRAPHICS_NEW_VIDEO = Function(
    name="newVideo",
    description="Creates a new Video object from a video file.",
    variants=[
        Variant(
            arguments=[
                Argument(type="string", name="filename", description="The video filename."),
            ],
            returns=[
                Return(type="Video", name="video", description="The created Video object."),
            ]
        )
    ]
)

GRAPHICS_NEW_MESH = Function(
    name="newMesh",
    description="Creates a new Mesh.",
    variants=[
        Variant(
            arguments=[
                Argument(type="table", name="vertices", description="Vertex data used to initialize the mesh."),
                Argument(type="MeshDrawMode", name="mode", description="How the mesh should be drawn.", default="triangles"),
                Argument(type="string", name="usage", description="Vertex storage usage hint.", default="dynamic"),
            ],
            returns=[
                Return(type="Mesh", name="mesh", description="The created Mesh."),
            ]
        ),
        Variant(
            arguments=[
                Argument(type="number", name="vertexcount", description="The number of vertices in the mesh."),
                Argument(type="MeshDrawMode", name="mode", description="How the mesh should be drawn.", default="triangles"),
                Argument(type="string", name="usage", description="Vertex storage usage hint.", default="dynamic"),
            ],
            returns=[
                Return(type="Mesh", name="mesh", description="The created Mesh."),
            ]
        ),
    ]
)

GRAPHICS_NEW_SPRITE_BATCH = Function(
    name="newSpriteBatch",
    description="Creates a new SpriteBatch.",
    variants=[
        Variant(
            arguments=[
                Argument(type="Image", name="texture", description="The image texture to use."),
                Argument(type="number", name="size", description="The maximum number of sprites.", default="1000"),
                Argument(type="string", name="usage", description="Vertex storage usage hint.", default="dynamic"),
            ],
            returns=[
                Return(type="SpriteBatch", name="batch", description="The created SpriteBatch."),
            ]
        )
    ]
)

GRAPHICS_NEW_PARTICLE_SYSTEM = Function(
    name="newParticleSystem",
    description="Creates a new ParticleSystem.",
    variants=[
        Variant(
            arguments=[
                Argument(type="Texture", name="texture", description="The texture to use for particles."),
                Argument(type="number", name="buffer", description="The maximum number of particles.", default="1000"),
            ],
            returns=[
                Return(type="ParticleSystem", name="system", description="The created ParticleSystem."),
            ]
        )
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

GRAPHICS_ARC = Function(
    name="arc",
    description="Draws an arc.",
    variants=[
        Variant(
            arguments=[
                Argument(type="DrawMode", name="mode", description="How to draw the arc."),
                Argument(type="ArcType", name="arctype", description="How to draw the arc."),
                Argument(type="number", name="x", description="The x-coordinate."),
                Argument(type="number", name="y", description="The y-coordinate."),
                Argument(type="number", name="radius", description="The radius of the arc."),
                Argument(type="number", name="angle1", description="The start angle in radians."),
                Argument(type="number", name="angle2", description="The end angle in radians."),
                Argument(type="number", name="segments", description="The number of segments used for drawing.", default="nil"),
            ]
        )
    ]
)

GRAPHICS_ELLIPSE = Function(
    name="ellipse",
    description="Draws an ellipse.",
    variants=[
        Variant(
            arguments=[
                Argument(type="DrawMode", name="mode", description="How to draw the ellipse."),
                Argument(type="number", name="x", description="The x-coordinate."),
                Argument(type="number", name="y", description="The y-coordinate."),
                Argument(type="number", name="radiusx", description="The radius on the x axis."),
                Argument(type="number", name="radiusy", description="The radius on the y axis.", default="radiusx"),
                Argument(type="number", name="segments", description="The number of segments used for drawing.", default="nil"),
            ]
        )
    ]
)

GRAPHICS_POINTS = Function(
    name="points",
    description="Draws points.",
    variants=[
        Variant(
            arguments=[
                Argument(type="number", name="x", description="The x-coordinate of the point."),
                Argument(type="number", name="y", description="The y-coordinate of the point."),
            ]
        ),
        Variant(
            arguments=[
                Argument(type="table", name="points", description="A table of points {x1, y1, x2, y2, ...}."),
            ]
        ),
    ]
)

GRAPHICS_POLYGON = Function(
    name="polygon",
    description="Draws a polygon.",
    variants=[
        Variant(
            arguments=[
                Argument(type="DrawMode", name="mode", description="How to draw the polygon."),
                Argument(type="table", name="vertices", description="A table of vertices {x1, y1, x2, y2, ...}."),
            ]
        ),
        Variant(
            arguments=[
                Argument(type="DrawMode", name="mode", description="How to draw the polygon."),
                Argument(type="number", name="x1", description="The x-coordinate of the first vertex."),
                Argument(type="number", name="y1", description="The y-coordinate of the first vertex."),
                Argument(type="number", name="...", description="Remaining vertex coordinates."),
            ]
        ),
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

GRAPHICS_APPLY_TRANSFORM = Function(
    name="applyTransform",
    description="Applies a Transform object to the current coordinate transformation.",
    variants=[
        Variant(
            arguments=[
                Argument(type="Transform", name="transform", description="The Transform to apply."),
            ]
        )
    ]
)

GRAPHICS_REPLACE_TRANSFORM = Function(
    name="replaceTransform",
    description="Replaces the current coordinate transformation with a Transform.",
    variants=[
        Variant(
            arguments=[
                Argument(type="Transform", name="transform", description="The Transform to replace with."),
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

GRAPHICS_CAPTURE_SCREENSHOT = Function(
    name="captureScreenshot",
    description="Captures a screenshot and saves it to a file.",
    variants=[
        Variant(
            arguments=[
                Argument(type="string", name="filename", description="The screenshot filename.", default="nil"),
            ]
        ),
        Variant(
            arguments=[
                Argument(type="function", name="callback", description="Callback which receives the ImageData."),
            ]
        ),
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

GRAPHICS_SET_SHADER = Function(
    name="setShader",
    description="Sets the active shader.",
    variants=[
        Variant(
            arguments=[
                Argument(type="Shader", name="shader", description="The shader to use.", default="nil"),
            ]
        )
    ]
)

GRAPHICS_GET_SHADER = Function(
    name="getShader",
    description="Gets the active shader.",
    variants=[
        Variant(
            returns=[
                Return(type="Shader", name="shader", description="The current shader, or nil."),
            ]
        )
    ]
)

GRAPHICS_SET_SCISSOR = Function(
    name="setScissor",
    description="Sets the scissor rectangle.",
    variants=[
        Variant(),
        Variant(
            arguments=[
                Argument(type="number", name="x", description="The x position of the scissor rectangle."),
                Argument(type="number", name="y", description="The y position of the scissor rectangle."),
                Argument(type="number", name="width", description="The width of the scissor rectangle."),
                Argument(type="number", name="height", description="The height of the scissor rectangle."),
            ]
        ),
    ]
)

GRAPHICS_GET_SCISSOR = Function(
    name="getScissor",
    description="Gets the scissor rectangle.",
    variants=[
        Variant(
            returns=[
                Return(type="number", name="x", description="The x position of the scissor rectangle, or nil."),
                Return(type="number", name="y", description="The y position of the scissor rectangle, or nil."),
                Return(type="number", name="width", description="The width of the scissor rectangle, or nil."),
                Return(type="number", name="height", description="The height of the scissor rectangle, or nil."),
            ]
        )
    ]
)

GRAPHICS_SET_STENCIL_TEST = Function(
    name="setStencilTest",
    description="Sets the stencil test.",
    variants=[
        Variant(),
        Variant(
            arguments=[
                Argument(type="CompareMode", name="comparemode", description="How to compare stencil values."),
                Argument(type="number", name="value", description="The value to compare against.", default="0"),
            ]
        ),
    ]
)

GRAPHICS_GET_STENCIL_TEST = Function(
    name="getStencilTest",
    description="Gets the current stencil test.",
    variants=[
        Variant(
            returns=[
                Return(type="CompareMode", name="comparemode", description="The current compare mode, or nil."),
                Return(type="number", name="value", description="The current stencil reference value, or nil."),
            ]
        )
    ]
)

GRAPHICS_SET_LINE_STYLE = Function(
    name="setLineStyle",
    description="Sets the line style.",
    variants=[
        Variant(
            arguments=[
                Argument(type="LineStyle", name="style", description="The line style."),
            ]
        )
    ]
)

GRAPHICS_GET_LINE_STYLE = Function(
    name="getLineStyle",
    description="Gets the line style.",
    variants=[
        Variant(
            returns=[
                Return(type="LineStyle", name="style", description="The current line style."),
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
        GRAPHICS_MESH_TYPE,
        GRAPHICS_SPRITE_BATCH_TYPE,
        GRAPHICS_PARTICLE_SYSTEM_TYPE,
        GRAPHICS_TEXT_TYPE,
        GRAPHICS_VIDEO_TYPE,
    ],
    functions=[
        GRAPHICS_NEW_IMAGE,
        GRAPHICS_NEW_CANVAS,
        GRAPHICS_NEW_FONT,
        GRAPHICS_NEW_QUAD,
        GRAPHICS_NEW_SHADER,
        GRAPHICS_NEW_IMAGE_FONT,
        GRAPHICS_NEW_TEXT,
        GRAPHICS_NEW_VIDEO,
        GRAPHICS_NEW_MESH,
        GRAPHICS_NEW_SPRITE_BATCH,
        GRAPHICS_NEW_PARTICLE_SYSTEM,
        GRAPHICS_DRAW,
        GRAPHICS_RECTANGLE,
        GRAPHICS_CIRCLE,
        GRAPHICS_ARC,
        GRAPHICS_ELLIPSE,
        GRAPHICS_POINTS,
        GRAPHICS_POLYGON,
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
        GRAPHICS_APPLY_TRANSFORM,
        GRAPHICS_REPLACE_TRANSFORM,
        GRAPHICS_ORIGIN,
        GRAPHICS_CLEAR,
        GRAPHICS_PRESENT,
        GRAPHICS_CAPTURE_SCREENSHOT,
        GRAPHICS_SET_CANVAS,
        GRAPHICS_GET_CANVAS,
        GRAPHICS_SET_FONT,
        GRAPHICS_GET_FONT,
        GRAPHICS_SET_SHADER,
        GRAPHICS_GET_SHADER,
        GRAPHICS_SET_SCISSOR,
        GRAPHICS_GET_SCISSOR,
        GRAPHICS_SET_STENCIL_TEST,
        GRAPHICS_GET_STENCIL_TEST,
        GRAPHICS_SET_LINE_WIDTH,
        GRAPHICS_GET_LINE_WIDTH,
        GRAPHICS_SET_LINE_STYLE,
        GRAPHICS_GET_LINE_STYLE,
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
        GRAPHICS_ALIGN_MODE_ENUM,
        GRAPHICS_BLEND_ALPHA_MODE_ENUM,
        GRAPHICS_LINE_STYLE_ENUM,
        GRAPHICS_LINE_JOIN_ENUM,
        GRAPHICS_STACK_TYPE_ENUM,
        GRAPHICS_MESH_DRAW_MODE_ENUM,
        GRAPHICS_COMPARE_MODE_ENUM,
        GRAPHICS_CULL_MODE_ENUM,
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

KEYBOARD_SCANCODE_ENUM = Enum(
    name="Scancode",
    description="Keyboard scancode constants.",
    constants=[
        EnumConstant(name="a", description=""),
        EnumConstant(name="b", description=""),
        EnumConstant(name="c", description=""),
        EnumConstant(name="d", description=""),
        EnumConstant(name="e", description=""),
        EnumConstant(name="f", description=""),
        EnumConstant(name="g", description=""),
        EnumConstant(name="h", description=""),
        EnumConstant(name="i", description=""),
        EnumConstant(name="j", description=""),
        EnumConstant(name="k", description=""),
        EnumConstant(name="l", description=""),
        EnumConstant(name="m", description=""),
        EnumConstant(name="n", description=""),
        EnumConstant(name="o", description=""),
        EnumConstant(name="p", description=""),
        EnumConstant(name="q", description=""),
        EnumConstant(name="r", description=""),
        EnumConstant(name="s", description=""),
        EnumConstant(name="t", description=""),
        EnumConstant(name="u", description=""),
        EnumConstant(name="v", description=""),
        EnumConstant(name="w", description=""),
        EnumConstant(name="x", description=""),
        EnumConstant(name="y", description=""),
        EnumConstant(name="z", description=""),
        EnumConstant(name="1", description=""),
        EnumConstant(name="2", description=""),
        EnumConstant(name="3", description=""),
        EnumConstant(name="4", description=""),
        EnumConstant(name="5", description=""),
        EnumConstant(name="6", description=""),
        EnumConstant(name="7", description=""),
        EnumConstant(name="8", description=""),
        EnumConstant(name="9", description=""),
        EnumConstant(name="0", description=""),
        EnumConstant(name="return", description=""),
        EnumConstant(name="escape", description=""),
        EnumConstant(name="backspace", description=""),
        EnumConstant(name="tab", description=""),
        EnumConstant(name="space", description=""),
        EnumConstant(name="minus", description=""),
        EnumConstant(name="equals", description=""),
        EnumConstant(name="leftbracket", description=""),
        EnumConstant(name="rightbracket", description=""),
        EnumConstant(name="backslash", description=""),
        EnumConstant(name="nonushash", description=""),
        EnumConstant(name="semicolon", description=""),
        EnumConstant(name="apostrophe", description=""),
        EnumConstant(name="grave", description=""),
        EnumConstant(name="comma", description=""),
        EnumConstant(name="period", description=""),
        EnumConstant(name="slash", description=""),
        EnumConstant(name="capslock", description=""),
        EnumConstant(name="f1", description=""),
        EnumConstant(name="f2", description=""),
        EnumConstant(name="f3", description=""),
        EnumConstant(name="f4", description=""),
        EnumConstant(name="f5", description=""),
        EnumConstant(name="f6", description=""),
        EnumConstant(name="f7", description=""),
        EnumConstant(name="f8", description=""),
        EnumConstant(name="f9", description=""),
        EnumConstant(name="f10", description=""),
        EnumConstant(name="f11", description=""),
        EnumConstant(name="f12", description=""),
        EnumConstant(name="printscreen", description=""),
        EnumConstant(name="scrolllock", description=""),
        EnumConstant(name="pause", description=""),
        EnumConstant(name="insert", description=""),
        EnumConstant(name="home", description=""),
        EnumConstant(name="pageup", description=""),
        EnumConstant(name="delete", description=""),
        EnumConstant(name="end", description=""),
        EnumConstant(name="pagedown", description=""),
        EnumConstant(name="right", description=""),
        EnumConstant(name="left", description=""),
        EnumConstant(name="down", description=""),
        EnumConstant(name="up", description=""),
        EnumConstant(name="numlockclear", description=""),
        EnumConstant(name="kp_divide", description=""),
        EnumConstant(name="kp_multiply", description=""),
        EnumConstant(name="kp_minus", description=""),
        EnumConstant(name="kp_plus", description=""),
        EnumConstant(name="kp_enter", description=""),
        EnumConstant(name="kp_1", description=""),
        EnumConstant(name="kp_2", description=""),
        EnumConstant(name="kp_3", description=""),
        EnumConstant(name="kp_4", description=""),
        EnumConstant(name="kp_5", description=""),
        EnumConstant(name="kp_6", description=""),
        EnumConstant(name="kp_7", description=""),
        EnumConstant(name="kp_8", description=""),
        EnumConstant(name="kp_9", description=""),
        EnumConstant(name="kp_0", description=""),
        EnumConstant(name="kp_period", description=""),
        EnumConstant(name="nonusbackslash", description=""),
        EnumConstant(name="application", description=""),
        EnumConstant(name="power", description=""),
        EnumConstant(name="kp_equals", description=""),
        EnumConstant(name="f13", description=""),
        EnumConstant(name="f14", description=""),
        EnumConstant(name="f15", description=""),
        EnumConstant(name="f16", description=""),
        EnumConstant(name="f17", description=""),
        EnumConstant(name="f18", description=""),
        EnumConstant(name="f19", description=""),
        EnumConstant(name="f20", description=""),
        EnumConstant(name="f21", description=""),
        EnumConstant(name="f22", description=""),
        EnumConstant(name="f23", description=""),
        EnumConstant(name="f24", description=""),
        EnumConstant(name="execute", description=""),
        EnumConstant(name="help", description=""),
        EnumConstant(name="menu", description=""),
        EnumConstant(name="select", description=""),
        EnumConstant(name="stop", description=""),
        EnumConstant(name="again", description=""),
        EnumConstant(name="undo", description=""),
        EnumConstant(name="cut", description=""),
        EnumConstant(name="copy", description=""),
        EnumConstant(name="paste", description=""),
        EnumConstant(name="find", description=""),
        EnumConstant(name="mute", description=""),
        EnumConstant(name="volumeup", description=""),
        EnumConstant(name="volumedown", description=""),
        EnumConstant(name="kp_comma", description=""),
        EnumConstant(name="kp_equalsas400", description=""),
        EnumConstant(name="international1", description=""),
        EnumConstant(name="international2", description=""),
        EnumConstant(name="international3", description=""),
        EnumConstant(name="international4", description=""),
        EnumConstant(name="international5", description=""),
        EnumConstant(name="international6", description=""),
        EnumConstant(name="international7", description=""),
        EnumConstant(name="international8", description=""),
        EnumConstant(name="international9", description=""),
        EnumConstant(name="lang1", description=""),
        EnumConstant(name="lang2", description=""),
        EnumConstant(name="lang3", description=""),
        EnumConstant(name="lang4", description=""),
        EnumConstant(name="lang5", description=""),
        EnumConstant(name="lang6", description=""),
        EnumConstant(name="lang7", description=""),
        EnumConstant(name="lang8", description=""),
        EnumConstant(name="lang9", description=""),
        EnumConstant(name="alterase", description=""),
        EnumConstant(name="sysreq", description=""),
        EnumConstant(name="cancel", description=""),
        EnumConstant(name="clear", description=""),
        EnumConstant(name="prior", description=""),
        EnumConstant(name="return2", description=""),
        EnumConstant(name="separator", description=""),
        EnumConstant(name="out", description=""),
        EnumConstant(name="oper", description=""),
        EnumConstant(name="clearagain", description=""),
        EnumConstant(name="crsel", description=""),
        EnumConstant(name="exsel", description=""),
        EnumConstant(name="kp_00", description=""),
        EnumConstant(name="kp_000", description=""),
        EnumConstant(name="thousandsseparator", description=""),
        EnumConstant(name="decimalseparator", description=""),
        EnumConstant(name="currencyunit", description=""),
        EnumConstant(name="currencysubunit", description=""),
        EnumConstant(name="kp_leftparen", description=""),
        EnumConstant(name="kp_rightparen", description=""),
        EnumConstant(name="kp_leftbrace", description=""),
        EnumConstant(name="kp_rightbrace", description=""),
        EnumConstant(name="kp_tab", description=""),
        EnumConstant(name="kp_backspace", description=""),
        EnumConstant(name="kp_a", description=""),
        EnumConstant(name="kp_b", description=""),
        EnumConstant(name="kp_c", description=""),
        EnumConstant(name="kp_d", description=""),
        EnumConstant(name="kp_e", description=""),
        EnumConstant(name="kp_f", description=""),
        EnumConstant(name="kp_xor", description=""),
        EnumConstant(name="kp_power", description=""),
        EnumConstant(name="kp_percent", description=""),
        EnumConstant(name="kp_less", description=""),
        EnumConstant(name="kp_greater", description=""),
        EnumConstant(name="kp_ampersand", description=""),
        EnumConstant(name="kp_dblampersand", description=""),
        EnumConstant(name="kp_verticalbar", description=""),
        EnumConstant(name="kp_dblverticalbar", description=""),
        EnumConstant(name="kp_colon", description=""),
        EnumConstant(name="kp_hash", description=""),
        EnumConstant(name="kp_space", description=""),
        EnumConstant(name="kp_at", description=""),
        EnumConstant(name="kp_exclam", description=""),
        EnumConstant(name="kp_memstore", description=""),
        EnumConstant(name="kp_memrecall", description=""),
        EnumConstant(name="kp_memclear", description=""),
        EnumConstant(name="kp_memadd", description=""),
        EnumConstant(name="kp_memsubtract", description=""),
        EnumConstant(name="kp_memmultiply", description=""),
        EnumConstant(name="kp_memdivide", description=""),
        EnumConstant(name="kp_plusminus", description=""),
        EnumConstant(name="kp_clear", description=""),
        EnumConstant(name="kp_clearentry", description=""),
        EnumConstant(name="kp_binary", description=""),
        EnumConstant(name="kp_octal", description=""),
        EnumConstant(name="kp_decimal", description=""),
        EnumConstant(name="kp_hexadecimal", description=""),
        EnumConstant(name="lctrl", description=""),
        EnumConstant(name="lshift", description=""),
        EnumConstant(name="lalt", description=""),
        EnumConstant(name="lgui", description=""),
        EnumConstant(name="rctrl", description=""),
        EnumConstant(name="rshift", description=""),
        EnumConstant(name="ralt", description=""),
        EnumConstant(name="rgui", description=""),
        EnumConstant(name="mode", description=""),
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
        KEYBOARD_SCANCODE_ENUM,
    ]
)

# ============================================================================
# Module: Mouse
# ============================================================================

MOUSE_CURSOR_TYPE_ENUM = Enum(
    name="CursorType",
    description="CursorType constants.",
    constants=[
        EnumConstant(name="arrow", description=""),
        EnumConstant(name="ibeam", description=""),
        EnumConstant(name="wait", description=""),
        EnumConstant(name="waitarrow", description=""),
        EnumConstant(name="crosshair", description=""),
        EnumConstant(name="sizenwse", description=""),
        EnumConstant(name="sizenesw", description=""),
        EnumConstant(name="sizewe", description=""),
        EnumConstant(name="sizens", description=""),
        EnumConstant(name="sizeall", description=""),
        EnumConstant(name="no", description=""),
        EnumConstant(name="hand", description=""),
    ]
)

MOUSE_CURSOR_TYPE = Type(
    name="Cursor",
    description="Mouse cursor object.",
    constructors=["newCursor", "getSystemCursor"],
    functions=[
        Function(name="getType", description="Method getType.", variants=[]),
    ],
    supertypes=["Object"]
)

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

MOUSE_IS_RELATIVE_MODE = Function(
    name="isRelativeMode",
    description="Gets whether the mouse is in relative mode.",
    variants=[
        Variant(
            returns=[
                Return(type="boolean", name="enabled", description="True if relative mode is enabled."),
            ]
        )
    ]
)

MOUSE_NEW_CURSOR = Function(
    name="newCursor",
    description="Creates a new Cursor from ImageData.",
    variants=[
        Variant(
            arguments=[
                Argument(type="ImageData", name="imagedata", description="The ImageData to use."),
                Argument(type="number", name="hotx", description="The x coordinate of the hot spot."),
                Argument(type="number", name="hoty", description="The y coordinate of the hot spot."),
            ],
            returns=[
                Return(type="Cursor", name="cursor", description="The created cursor."),
            ]
        )
    ]
)

MOUSE_GET_SYSTEM_CURSOR = Function(
    name="getSystemCursor",
    description="Gets a system Cursor.",
    variants=[
        Variant(
            arguments=[
                Argument(type="CursorType", name="cursor", description="The system cursor type."),
            ],
            returns=[
                Return(type="Cursor", name="cursor", description="The system cursor."),
            ]
        )
    ]
)

MOUSE_SET_CURSOR = Function(
    name="setCursor",
    description="Sets the current Cursor.",
    variants=[
        Variant(
            arguments=[
                Argument(type="Cursor", name="cursor", description="The cursor to set.", default="nil"),
            ]
        )
    ]
)

MOUSE_GET_CURSOR = Function(
    name="getCursor",
    description="Gets the current Cursor.",
    variants=[
        Variant(
            returns=[
                Return(type="Cursor", name="cursor", description="The current cursor, or nil."),
            ]
        )
    ]
)

# Mouse Module
MOUSE_MODULE = Module(
    name="mouse",
    description="Provides an interface to the user's mouse.",
    types=[
        MOUSE_CURSOR_TYPE,
    ],
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
        MOUSE_IS_RELATIVE_MODE,
        MOUSE_NEW_CURSOR,
        MOUSE_GET_SYSTEM_CURSOR,
        MOUSE_SET_CURSOR,
        MOUSE_GET_CURSOR,
    ],
    enums=[
        MOUSE_CURSOR_TYPE_ENUM,
    ]
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

TIMER_STEP = Function(
    name="step",
    description="Advances the internal timer and returns the time since the last step.",
    variants=[
        Variant(
            returns=[
                Return(type="number", name="dt", description="Time since the previous step in seconds."),
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
        TIMER_STEP,
    ],
    enums=[]
)

# ============================================================================
# Module: Window
# ============================================================================

WINDOW_FULLSCREEN_TYPE_ENUM = Enum(
    name="FullscreenType",
    description="FullscreenType constants.",
    constants=[
        EnumConstant(name="exclusive", description=""),
        EnumConstant(name="desktop", description=""),
    ]
)

WINDOW_MESSAGE_BOX_TYPE_ENUM = Enum(
    name="MessageBoxType",
    description="MessageBoxType constants.",
    constants=[
        EnumConstant(name="info", description=""),
        EnumConstant(name="warning", description=""),
        EnumConstant(name="error", description=""),
    ]
)

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

WINDOW_MAXIMIZE = Function(
    name="maximize",
    description="Maximizes the window.",
    variants=[
        Variant()
    ]
)

WINDOW_MINIMIZE = Function(
    name="minimize",
    description="Minimizes the window.",
    variants=[
        Variant()
    ]
)

WINDOW_RESTORE = Function(
    name="restore",
    description="Restores the window to its previous state.",
    variants=[
        Variant()
    ]
)

WINDOW_HAS_FOCUS = Function(
    name="hasFocus",
    description="Gets whether the window has focus.",
    variants=[
        Variant(
            returns=[
                Return(type="boolean", name="focused", description="True if the window has focus."),
            ]
        )
    ]
)

WINDOW_HAS_MOUSE_FOCUS = Function(
    name="hasMouseFocus",
    description="Gets whether the window has mouse focus.",
    variants=[
        Variant(
            returns=[
                Return(type="boolean", name="focused", description="True if the window has mouse focus."),
            ]
        )
    ]
)

WINDOW_IS_DISPLAY_SLEEP_ENABLED = Function(
    name="isDisplaySleepEnabled",
    description="Gets whether the system is allowed to sleep.",
    variants=[
        Variant(
            returns=[
                Return(type="boolean", name="enabled", description="True if display sleep is enabled."),
            ]
        )
    ]
)

WINDOW_SET_DISPLAY_SLEEP_ENABLED = Function(
    name="setDisplaySleepEnabled",
    description="Sets whether the system is allowed to sleep.",
    variants=[
        Variant(
            arguments=[
                Argument(type="boolean", name="enable", description="Whether to enable display sleep."),
            ]
        )
    ]
)

WINDOW_GET_DPI_SCALE = Function(
    name="getDPIScale",
    description="Gets the DPI scale factor of the window.",
    variants=[
        Variant(
            returns=[
                Return(type="number", name="scale", description="The DPI scale factor."),
            ]
        )
    ]
)

WINDOW_TO_PIXELS = Function(
    name="toPixels",
    description="Converts from units to pixels based on DPI scaling.",
    variants=[
        Variant(
            arguments=[
                Argument(type="number", name="x", description="The x value to convert."),
            ],
            returns=[
                Return(type="number", name="px", description="The x value in pixels."),
            ]
        ),
        Variant(
            arguments=[
                Argument(type="number", name="x", description="The x value to convert."),
                Argument(type="number", name="y", description="The y value to convert."),
            ],
            returns=[
                Return(type="number", name="px", description="The x value in pixels."),
                Return(type="number", name="py", description="The y value in pixels."),
            ]
        ),
    ]
)

WINDOW_FROM_PIXELS = Function(
    name="fromPixels",
    description="Converts from pixels to units based on DPI scaling.",
    variants=[
        Variant(
            arguments=[
                Argument(type="number", name="px", description="The x value in pixels."),
            ],
            returns=[
                Return(type="number", name="x", description="The x value in units."),
            ]
        ),
        Variant(
            arguments=[
                Argument(type="number", name="px", description="The x value in pixels."),
                Argument(type="number", name="py", description="The y value in pixels."),
            ],
            returns=[
                Return(type="number", name="x", description="The x value in units."),
                Return(type="number", name="y", description="The y value in units."),
            ]
        ),
    ]
)

WINDOW_GET_DESKTOP_DIMENSIONS = Function(
    name="getDesktopDimensions",
    description="Gets the width and height of the desktop on a display.",
    variants=[
        Variant(
            arguments=[
                Argument(type="number", name="display", description="The display index.", default="1"),
            ],
            returns=[
                Return(type="number", name="width", description="The desktop width in pixels."),
                Return(type="number", name="height", description="The desktop height in pixels."),
            ]
        )
    ]
)

WINDOW_GET_DISPLAY_COUNT = Function(
    name="getDisplayCount",
    description="Gets the number of connected displays.",
    variants=[
        Variant(
            returns=[
                Return(type="number", name="count", description="The number of displays."),
            ]
        )
    ]
)

WINDOW_GET_DISPLAY_NAME = Function(
    name="getDisplayName",
    description="Gets the name of a display.",
    variants=[
        Variant(
            arguments=[
                Argument(type="number", name="display", description="The display index.", default="1"),
            ],
            returns=[
                Return(type="string", name="name", description="The display name."),
            ]
        )
    ]
)

WINDOW_GET_DISPLAY_ORIENTATION = Function(
    name="getDisplayOrientation",
    description="Gets the orientation of a display.",
    variants=[
        Variant(
            arguments=[
                Argument(type="number", name="display", description="The display index.", default="1"),
            ],
            returns=[
                Return(type="string", name="orientation", description="The display orientation."),
            ]
        )
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
        WINDOW_GET_DPI_SCALE,
        WINDOW_TO_PIXELS,
        WINDOW_FROM_PIXELS,
        WINDOW_GET_DESKTOP_DIMENSIONS,
        WINDOW_GET_DISPLAY_COUNT,
        WINDOW_GET_DISPLAY_NAME,
        WINDOW_GET_DISPLAY_ORIENTATION,
        WINDOW_HAS_FOCUS,
        WINDOW_HAS_MOUSE_FOCUS,
        WINDOW_IS_DISPLAY_SLEEP_ENABLED,
        WINDOW_SET_DISPLAY_SLEEP_ENABLED,
        WINDOW_SHOW_MESSAGE_BOX,
        WINDOW_MAXIMIZE,
        WINDOW_MINIMIZE,
        WINDOW_RESTORE,
        WINDOW_CLOSE,
    ],
    enums=[
        WINDOW_FULLSCREEN_TYPE_ENUM,
        WINDOW_MESSAGE_BOX_TYPE_ENUM,
    ]
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

EVENT_QUIT = Function(
    name="quit",
    description="Queues a quit event.",
    variants=[
        Variant(
            arguments=[
                Argument(type="number", name="exitstatus", description="The exit status code.", default="0"),
            ]
        )
    ]
)

EVENT_PUSH = Function(
    name="push",
    description="Pushes an event onto the event queue.",
    variants=[
        Variant(
            arguments=[
                Argument(type="string", name="name", description="The name of the event."),
                Argument(type="mixed", name="...", description="Additional event arguments.", default="nil"),
            ],
            returns=[
                Return(type="boolean", name="success", description="True if successful."),
            ]
        )
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
        EVENT_QUIT,
        EVENT_PUSH,
    ],
    enums=[]
)

# ============================================================================
# Module: Filesystem
# ============================================================================

FILESYSTEM_FILE_MODE_ENUM = Enum(
    name="FileMode",
    description="FileMode constants.",
    constants=[
        EnumConstant(name="r", description=""),
        EnumConstant(name="w", description=""),
        EnumConstant(name="a", description=""),
        EnumConstant(name="c", description=""),
    ]
)

FILESYSTEM_FILE_TYPE_ENUM = Enum(
    name="FileType",
    description="FileType constants.",
    constants=[
        EnumConstant(name="file", description=""),
        EnumConstant(name="directory", description=""),
        EnumConstant(name="symlink", description=""),
        EnumConstant(name="other", description=""),
    ]
)

FILESYSTEM_BUFFER_MODE_ENUM = Enum(
    name="BufferMode",
    description="BufferMode constants.",
    constants=[
        EnumConstant(name="none", description=""),
        EnumConstant(name="line", description=""),
        EnumConstant(name="full", description=""),
    ]
)

FILESYSTEM_FILE_TYPE = Type(
    name="File",
    description="File object.",
    constructors=["newFile", "openFile"],
    functions=[
        Function(name="open", description="Method open.", variants=[]),
        Function(name="close", description="Method close.", variants=[]),
        Function(name="read", description="Method read.", variants=[]),
        Function(name="write", description="Method write.", variants=[]),
        Function(name="flush", description="Method flush.", variants=[]),
        Function(name="isOpen", description="Method isOpen.", variants=[]),
        Function(name="getSize", description="Method getSize.", variants=[]),
        Function(name="getMode", description="Method getMode.", variants=[]),
        Function(name="seek", description="Method seek.", variants=[]),
        Function(name="tell", description="Method tell.", variants=[]),
        Function(name="getFilename", description="Method getFilename.", variants=[]),
        Function(name="getBuffer", description="Method getBuffer.", variants=[]),
        Function(name="setBuffer", description="Method setBuffer.", variants=[]),
    ],
    supertypes=["Object"]
)

FILESYSTEM_FILE_DATA_TYPE = Type(
    name="FileData",
    description="FileData object.",
    constructors=["newFileData"],
    functions=[
        Function(name="getString", description="Method getString.", variants=[]),
        Function(name="getFilename", description="Method getFilename.", variants=[]),
        Function(name="getExtension", description="Method getExtension.", variants=[]),
    ],
    supertypes=["Object"]
)

FILESYSTEM_DROPPED_FILE_TYPE = Type(
    name="DroppedFile",
    description="DroppedFile object.",
    constructors=[],
    functions=[
        Function(name="open", description="Method open.", variants=[]),
        Function(name="close", description="Method close.", variants=[]),
        Function(name="read", description="Method read.", variants=[]),
        Function(name="write", description="Method write.", variants=[]),
        Function(name="isOpen", description="Method isOpen.", variants=[]),
    ],
    supertypes=["Object"]
)

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

FILESYSTEM_GET_EXECUTABLE_PATH = Function(
    name="getExecutablePath",
    description="Returns the path to the LÖVE executable.",
    variants=[
        Variant(
            returns=[
                Return(type="string", name="path", description="The full path to the executable."),
            ]
        )
    ]
)

FILESYSTEM_GET_USER_DIRECTORY = Function(
    name="getUserDirectory",
    description="Gets the user's home directory.",
    variants=[
        Variant(
            returns=[
                Return(type="string", name="path", description="The user's home directory."),
            ]
        )
    ]
)

FILESYSTEM_GET_REAL_DIRECTORY = Function(
    name="getRealDirectory",
    description="Gets the actual directory containing a file.",
    variants=[
        Variant(
            arguments=[
                Argument(type="string", name="filename", description="The filename to locate."),
            ],
            returns=[
                Return(type="string", name="dir", description="The real directory containing the file, or nil."),
            ]
        )
    ]
)

FILESYSTEM_NEW_FILE = Function(
    name="newFile",
    description="Creates a new File object.",
    variants=[
        Variant(
            arguments=[
                Argument(type="string", name="filename", description="The filename of the File."),
            ],
            returns=[
                Return(type="File", name="file", description="The created File object."),
            ]
        )
    ]
)

FILESYSTEM_OPEN_FILE = Function(
    name="openFile",
    description="Opens a File object for the given path.",
    variants=[
        Variant(
            arguments=[
                Argument(type="string", name="filename", description="The filename to open."),
                Argument(type="FileMode", name="mode", description="The open mode.", default="r"),
            ],
            returns=[
                Return(type="File", name="file", description="The opened File object."),
            ]
        )
    ]
)

FILESYSTEM_NEW_FILE_DATA = Function(
    name="newFileData",
    description="Creates a new FileData object.",
    variants=[
        Variant(
            arguments=[
                Argument(type="string", name="contents", description="The contents of the file."),
                Argument(type="string", name="filename", description="The name of the FileData."),
                Argument(type="string", name="decoder", description="Optional decoder.", default="nil"),
            ],
            returns=[
                Return(type="FileData", name="filedata", description="The created FileData."),
            ]
        ),
        Variant(
            arguments=[
                Argument(type="File", name="file", description="A File to read from."),
                Argument(type="string", name="filename", description="The name of the FileData."),
            ],
            returns=[
                Return(type="FileData", name="filedata", description="The created FileData."),
            ]
        ),
    ]
)

FILESYSTEM_MOUNT = Function(
    name="mount",
    description="Mounts a zip file or directory as the game's filesystem.",
    variants=[
        Variant(
            arguments=[
                Argument(type="string", name="archive", description="The path to the archive or directory."),
                Argument(type="string", name="mountpoint", description="The mount point inside the virtual filesystem."),
                Argument(type="boolean", name="appendToPath", description="Whether to append to the search path.", default="false"),
            ],
            returns=[
                Return(type="boolean", name="success", description="True if successful."),
            ]
        )
    ]
)

FILESYSTEM_UNMOUNT = Function(
    name="unmount",
    description="Unmounts a previously mounted archive or directory.",
    variants=[
        Variant(
            arguments=[
                Argument(type="string", name="archive", description="The path to the archive or directory."),
            ],
            returns=[
                Return(type="boolean", name="success", description="True if successful."),
            ]
        )
    ]
)

FILESYSTEM_LOAD = Function(
    name="load",
    description="Loads a Lua file and returns it as a function.",
    variants=[
        Variant(
            arguments=[
                Argument(type="string", name="filename", description="The filename to load."),
            ],
            returns=[
                Return(type="function", name="chunk", description="The loaded chunk, or nil on failure."),
                Return(type="string", name="errormsg", description="The error message on failure."),
            ]
        )
    ]
)

FILESYSTEM_IS_FUSED = Function(
    name="isFused",
    description="Gets whether the game is fused.",
    variants=[
        Variant(
            returns=[
                Return(type="boolean", name="fused", description="True if fused."),
            ]
        )
    ]
)

FILESYSTEM_SET_FUSED = Function(
    name="setFused",
    description="Sets whether the game is fused.",
    variants=[
        Variant(
            arguments=[
                Argument(type="boolean", name="fused", description="Whether the game should be fused."),
            ]
        )
    ]
)

FILESYSTEM_MODULE = Module(
    name="filesystem",
    description="Provides an interface to the user's filesystem.",
    types=[
        FILESYSTEM_FILE_TYPE,
        FILESYSTEM_FILE_DATA_TYPE,
        FILESYSTEM_DROPPED_FILE_TYPE,
    ],
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
        FILESYSTEM_GET_EXECUTABLE_PATH,
        FILESYSTEM_GET_USER_DIRECTORY,
        FILESYSTEM_GET_REAL_DIRECTORY,
        FILESYSTEM_IS_FUSED,
        FILESYSTEM_SET_FUSED,
        FILESYSTEM_LOAD,
        FILESYSTEM_MOUNT,
        FILESYSTEM_UNMOUNT,
        FILESYSTEM_NEW_FILE,
        FILESYSTEM_OPEN_FILE,
        FILESYSTEM_NEW_FILE_DATA,
    ],
    enums=[
        FILESYSTEM_FILE_MODE_ENUM,
        FILESYSTEM_FILE_TYPE_ENUM,
        FILESYSTEM_BUFFER_MODE_ENUM,
    ]
)

# ============================================================================
# Module: Audio
# ============================================================================

AUDIO_SOURCE_TYPE_ENUM = Enum(
    name="SourceType",
    description="SourceType constants.",
    constants=[
        EnumConstant(name="static", description=""),
        EnumConstant(name="stream", description=""),
        EnumConstant(name="queue", description=""),
    ]
)

AUDIO_TIME_UNIT_ENUM = Enum(
    name="TimeUnit",
    description="TimeUnit constants.",
    constants=[
        EnumConstant(name="seconds", description=""),
        EnumConstant(name="samples", description=""),
    ]
)

AUDIO_DISTANCE_MODEL_ENUM = Enum(
    name="DistanceModel",
    description="DistanceModel constants.",
    constants=[
        EnumConstant(name="none", description=""),
        EnumConstant(name="inverse", description=""),
        EnumConstant(name="inverseclamped", description=""),
        EnumConstant(name="linear", description=""),
        EnumConstant(name="linearclamped", description=""),
        EnumConstant(name="exponent", description=""),
        EnumConstant(name="exponentclamped", description=""),
    ]
)

AUDIO_SOURCE_TYPE = Type(
    name="Source",
    description="Audio Source object.",
    constructors=["newSource"],
    functions=[
        Function(name="play", description="Method play.", variants=[]),
        Function(name="stop", description="Method stop.", variants=[]),
        Function(name="pause", description="Method pause.", variants=[]),
        Function(name="resume", description="Method resume.", variants=[]),
        Function(name="rewind", description="Method rewind.", variants=[]),
        Function(name="isPlaying", description="Method isPlaying.", variants=[]),
        Function(name="isPaused", description="Method isPaused.", variants=[]),
        Function(name="isStopped", description="Method isStopped.", variants=[]),
        Function(name="setVolume", description="Method setVolume.", variants=[]),
        Function(name="getVolume", description="Method getVolume.", variants=[]),
        Function(name="setPitch", description="Method setPitch.", variants=[]),
        Function(name="getPitch", description="Method getPitch.", variants=[]),
        Function(name="setLooping", description="Method setLooping.", variants=[]),
        Function(name="isLooping", description="Method isLooping.", variants=[]),
        Function(name="setPosition", description="Method setPosition.", variants=[]),
        Function(name="getPosition", description="Method getPosition.", variants=[]),
        Function(name="setVelocity", description="Method setVelocity.", variants=[]),
        Function(name="getVelocity", description="Method getVelocity.", variants=[]),
        Function(name="seek", description="Method seek.", variants=[]),
        Function(name="tell", description="Method tell.", variants=[]),
        Function(name="getDuration", description="Method getDuration.", variants=[]),
        Function(name="setVolumeLimits", description="Method setVolumeLimits.", variants=[]),
        Function(name="getVolumeLimits", description="Method getVolumeLimits.", variants=[]),
        Function(name="setAttenuationDistances", description="Method setAttenuationDistances.", variants=[]),
        Function(name="getAttenuationDistances", description="Method getAttenuationDistances.", variants=[]),
        Function(name="setRolloff", description="Method setRolloff.", variants=[]),
        Function(name="getRolloff", description="Method getRolloff.", variants=[]),
        Function(name="setCone", description="Method setCone.", variants=[]),
        Function(name="getCone", description="Method getCone.", variants=[]),
        Function(name="setDirection", description="Method setDirection.", variants=[]),
        Function(name="getDirection", description="Method getDirection.", variants=[]),
        Function(name="setRelative", description="Method setRelative.", variants=[]),
        Function(name="isRelative", description="Method isRelative.", variants=[]),
    ],
    supertypes=["Object"]
)

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

AUDIO_SET_VELOCITY = Function(
    name="setVelocity",
    description="Sets the velocity of the listener.",
    variants=[
        Variant(
            arguments=[
                Argument(type="number", name="x", description="The x velocity."),
                Argument(type="number", name="y", description="The y velocity."),
                Argument(type="number", name="z", description="The z velocity.", default="0"),
            ]
        )
    ]
)

AUDIO_GET_VELOCITY = Function(
    name="getVelocity",
    description="Gets the velocity of the listener.",
    variants=[
        Variant(
            returns=[
                Return(type="number", name="x", description="The x velocity."),
                Return(type="number", name="y", description="The y velocity."),
                Return(type="number", name="z", description="The z velocity."),
            ]
        )
    ]
)

AUDIO_SET_ORIENTATION = Function(
    name="setOrientation",
    description="Sets the orientation of the listener.",
    variants=[
        Variant(
            arguments=[
                Argument(type="number", name="fx", description="The forward vector x component."),
                Argument(type="number", name="fy", description="The forward vector y component."),
                Argument(type="number", name="fz", description="The forward vector z component."),
                Argument(type="number", name="ux", description="The up vector x component."),
                Argument(type="number", name="uy", description="The up vector y component."),
                Argument(type="number", name="uz", description="The up vector z component."),
            ]
        )
    ]
)

AUDIO_GET_ORIENTATION = Function(
    name="getOrientation",
    description="Gets the orientation of the listener.",
    variants=[
        Variant(
            returns=[
                Return(type="number", name="fx", description="The forward vector x component."),
                Return(type="number", name="fy", description="The forward vector y component."),
                Return(type="number", name="fz", description="The forward vector z component."),
                Return(type="number", name="ux", description="The up vector x component."),
                Return(type="number", name="uy", description="The up vector y component."),
                Return(type="number", name="uz", description="The up vector z component."),
            ]
        )
    ]
)

AUDIO_SET_DISTANCE_MODEL = Function(
    name="setDistanceModel",
    description="Sets the distance attenuation model.",
    variants=[
        Variant(
            arguments=[
                Argument(type="DistanceModel", name="model", description="The distance model."),
            ]
        )
    ]
)

AUDIO_GET_DISTANCE_MODEL = Function(
    name="getDistanceModel",
    description="Gets the distance attenuation model.",
    variants=[
        Variant(
            returns=[
                Return(type="DistanceModel", name="model", description="The current distance model."),
            ]
        )
    ]
)

AUDIO_GET_SOURCE_COUNT = Function(
    name="getSourceCount",
    description="Gets the total number of Sources.",
    variants=[
        Variant(
            returns=[
                Return(type="number", name="count", description="The total number of Sources."),
            ]
        )
    ]
)

AUDIO_GET_ACTIVE_SOURCE_COUNT = Function(
    name="getActiveSourceCount",
    description="Gets the number of actively playing Sources.",
    variants=[
        Variant(
            returns=[
                Return(type="number", name="count", description="The number of active Sources."),
            ]
        )
    ]
)

AUDIO_SET_EFFECT = Function(
    name="setEffect",
    description="Sets an audio effect.",
    variants=[
        Variant(
            arguments=[
                Argument(type="string", name="name", description="The name of the effect."),
                Argument(type="table", name="settings", description="Effect settings, or nil to disable.", default="nil"),
            ],
            returns=[
                Return(type="boolean", name="success", description="True if successful."),
            ]
        )
    ]
)

AUDIO_GET_EFFECT = Function(
    name="getEffect",
    description="Gets the settings of an audio effect.",
    variants=[
        Variant(
            arguments=[
                Argument(type="string", name="name", description="The name of the effect."),
            ],
            returns=[
                Return(type="table", name="settings", description="The effect settings, or nil."),
            ]
        )
    ]
)

AUDIO_REMOVE_EFFECT = Function(
    name="removeEffect",
    description="Removes an audio effect.",
    variants=[
        Variant(
            arguments=[
                Argument(type="string", name="name", description="The name of the effect."),
            ],
            returns=[
                Return(type="boolean", name="success", description="True if successful."),
            ]
        )
    ]
)

AUDIO_GET_RECORDING_DEVICES = Function(
    name="getRecordingDevices",
    description="Gets available audio recording devices.",
    variants=[
        Variant(
            returns=[
                Return(type="table", name="devices", description="A table of recording devices."),
            ]
        )
    ]
)

AUDIO_MODULE = Module(
    name="audio",
    description="Provides an interface to output audio to the user's speakers.",
    types=[
        AUDIO_SOURCE_TYPE,
    ],
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
        AUDIO_SET_VELOCITY,
        AUDIO_GET_VELOCITY,
        AUDIO_SET_ORIENTATION,
        AUDIO_GET_ORIENTATION,
        AUDIO_SET_DISTANCE_MODEL,
        AUDIO_GET_DISTANCE_MODEL,
        AUDIO_GET_SOURCE_COUNT,
        AUDIO_GET_ACTIVE_SOURCE_COUNT,
        AUDIO_SET_EFFECT,
        AUDIO_GET_EFFECT,
        AUDIO_REMOVE_EFFECT,
        AUDIO_GET_RECORDING_DEVICES,
    ],
    enums=[
        AUDIO_SOURCE_TYPE_ENUM,
        AUDIO_TIME_UNIT_ENUM,
        AUDIO_DISTANCE_MODEL_ENUM,
    ]
)

# ============================================================================
# Module: Math
# ============================================================================

MATH_TRANSFORM_TYPE = Type(
    name="Transform",
    description="Transform object.",
    constructors=["newTransform"],
    functions=[
        Function(name="setTransformation", description="Method setTransformation.", variants=[]),
        Function(name="translate", description="Method translate.", variants=[]),
        Function(name="rotate", description="Method rotate.", variants=[]),
        Function(name="scale", description="Method scale.", variants=[]),
        Function(name="shear", description="Method shear.", variants=[]),
        Function(name="apply", description="Method apply.", variants=[]),
        Function(name="reset", description="Method reset.", variants=[]),
        Function(name="inverse", description="Method inverse.", variants=[]),
        Function(name="clone", description="Method clone.", variants=[]),
        Function(name="getMatrix", description="Method getMatrix.", variants=[]),
    ],
    supertypes=["Object"]
)

MATH_BEZIER_CURVE_TYPE = Type(
    name="BezierCurve",
    description="BezierCurve object.",
    constructors=["newBezierCurve"],
    functions=[
        Function(name="getDegree", description="Method getDegree.", variants=[]),
        Function(name="getControlPoint", description="Method getControlPoint.", variants=[]),
        Function(name="setControlPoint", description="Method setControlPoint.", variants=[]),
        Function(name="insertControlPoint", description="Method insertControlPoint.", variants=[]),
        Function(name="removeControlPoint", description="Method removeControlPoint.", variants=[]),
        Function(name="getDerivative", description="Method getDerivative.", variants=[]),
        Function(name="getSegment", description="Method getSegment.", variants=[]),
        Function(name="render", description="Method render.", variants=[]),
        Function(name="renderSegment", description="Method renderSegment.", variants=[]),
    ],
    supertypes=["Object"]
)

MATH_RANDOM_GENERATOR_TYPE = Type(
    name="RandomGenerator",
    description="RandomGenerator object.",
    constructors=["newRandomGenerator"],
    functions=[
        Function(name="random", description="Method random.", variants=[]),
        Function(name="setSeed", description="Method setSeed.", variants=[]),
        Function(name="getSeed", description="Method getSeed.", variants=[]),
        Function(name="randomNormal", description="Method randomNormal.", variants=[]),
    ],
    supertypes=["Object"]
)

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

MATH_NOISE = Function(
    name="noise",
    description="Generates a simplex noise value.",
    variants=[
        Variant(
            arguments=[
                Argument(type="number", name="x", description="The x coordinate."),
            ],
            returns=[
                Return(type="number", name="value", description="The noise value."),
            ]
        ),
        Variant(
            arguments=[
                Argument(type="number", name="x", description="The x coordinate."),
                Argument(type="number", name="y", description="The y coordinate."),
            ],
            returns=[
                Return(type="number", name="value", description="The noise value."),
            ]
        ),
        Variant(
            arguments=[
                Argument(type="number", name="x", description="The x coordinate."),
                Argument(type="number", name="y", description="The y coordinate."),
                Argument(type="number", name="z", description="The z coordinate."),
            ],
            returns=[
                Return(type="number", name="value", description="The noise value."),
            ]
        ),
        Variant(
            arguments=[
                Argument(type="number", name="x", description="The x coordinate."),
                Argument(type="number", name="y", description="The y coordinate."),
                Argument(type="number", name="z", description="The z coordinate."),
                Argument(type="number", name="w", description="The w coordinate."),
            ],
            returns=[
                Return(type="number", name="value", description="The noise value."),
            ]
        ),
    ]
)

MATH_MODULE = Module(
    name="math",
    description="Provides system-independent mathematical functions.",
    types=[
        MATH_TRANSFORM_TYPE,
        MATH_BEZIER_CURVE_TYPE,
        MATH_RANDOM_GENERATOR_TYPE,
    ],
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
        MATH_NOISE,
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

JOYSTICK_GAMEPAD_AXIS_ENUM = Enum(
    name="GamepadAxis",
    description="GamepadAxis constants.",
    constants=[
        EnumConstant(name="leftx", description=""),
        EnumConstant(name="lefty", description=""),
        EnumConstant(name="rightx", description=""),
        EnumConstant(name="righty", description=""),
        EnumConstant(name="triggerleft", description=""),
        EnumConstant(name="triggerright", description=""),
    ]
)

JOYSTICK_GAMEPAD_BUTTON_ENUM = Enum(
    name="GamepadButton",
    description="GamepadButton constants.",
    constants=[
        EnumConstant(name="a", description=""),
        EnumConstant(name="b", description=""),
        EnumConstant(name="x", description=""),
        EnumConstant(name="y", description=""),
        EnumConstant(name="back", description=""),
        EnumConstant(name="guide", description=""),
        EnumConstant(name="start", description=""),
        EnumConstant(name="leftstick", description=""),
        EnumConstant(name="rightstick", description=""),
        EnumConstant(name="leftshoulder", description=""),
        EnumConstant(name="rightshoulder", description=""),
        EnumConstant(name="dpup", description=""),
        EnumConstant(name="dpdown", description=""),
        EnumConstant(name="dpleft", description=""),
        EnumConstant(name="dpright", description=""),
    ]
)

JOYSTICK_HAT_ENUM = Enum(
    name="JoystickHat",
    description="JoystickHat constants.",
    constants=[
        EnumConstant(name="c", description=""),
        EnumConstant(name="u", description=""),
        EnumConstant(name="r", description=""),
        EnumConstant(name="d", description=""),
        EnumConstant(name="lu", description=""),
        EnumConstant(name="ru", description=""),
        EnumConstant(name="ld", description=""),
        EnumConstant(name="rd", description=""),
    ]
)

JOYSTICK_INPUT_TYPE_ENUM = Enum(
    name="JoystickInputType",
    description="JoystickInputType constants.",
    constants=[
        EnumConstant(name="axis", description=""),
        EnumConstant(name="button", description=""),
        EnumConstant(name="hat", description=""),
    ]
)

JOYSTICK_TYPE = Type(
    name="Joystick",
    description="Joystick object.",
    constructors=[],
    functions=[
        Function(name="getName", description="Method getName.", variants=[]),
        Function(name="isConnected", description="Method isConnected.", variants=[]),
        Function(name="getID", description="Method getID.", variants=[]),
        Function(name="getGUID", description="Method getGUID.", variants=[]),
        Function(name="getAxisCount", description="Method getAxisCount.", variants=[]),
        Function(name="getButtonCount", description="Method getButtonCount.", variants=[]),
        Function(name="getHatCount", description="Method getHatCount.", variants=[]),
        Function(name="getAxis", description="Method getAxis.", variants=[]),
        Function(name="getAxes", description="Method getAxes.", variants=[]),
        Function(name="getHat", description="Method getHat.", variants=[]),
        Function(name="isDown", description="Method isDown.", variants=[]),
        Function(name="setVibration", description="Method setVibration.", variants=[]),
        Function(name="getVibration", description="Method getVibration.", variants=[]),
        Function(name="hasSensor", description="Method hasSensor.", variants=[]),
        Function(name="isSensorEnabled", description="Method isSensorEnabled.", variants=[]),
        Function(name="setSensorEnabled", description="Method setSensorEnabled.", variants=[]),
        Function(name="getSensorData", description="Method getSensorData.", variants=[]),
    ],
    supertypes=["Object"]
)

JOYSTICK_MODULE = Module(
    name="joystick",
    description="Provides an interface to gamepads and joysticks.",
    types=[
        JOYSTICK_TYPE,
    ],
    functions=[],
    enums=[
        JOYSTICK_GAMEPAD_AXIS_ENUM,
        JOYSTICK_GAMEPAD_BUTTON_ENUM,
        JOYSTICK_HAT_ENUM,
        JOYSTICK_INPUT_TYPE_ENUM,
    ]
)

IMAGE_PIXEL_FORMAT_ENUM = Enum(
    name="PixelFormat",
    description="PixelFormat constants.",
    constants=[
        EnumConstant(name="normal", description=""),
        EnumConstant(name="r8", description=""),
        EnumConstant(name="rg8", description=""),
        EnumConstant(name="rgba8", description=""),
        EnumConstant(name="srgba8", description=""),
        EnumConstant(name="r16", description=""),
        EnumConstant(name="rg16", description=""),
        EnumConstant(name="rgba16", description=""),
        EnumConstant(name="r16f", description=""),
        EnumConstant(name="rg16f", description=""),
        EnumConstant(name="rgba16f", description=""),
        EnumConstant(name="r32f", description=""),
        EnumConstant(name="rg32f", description=""),
        EnumConstant(name="rgba32f", description=""),
        EnumConstant(name="la8", description=""),
        EnumConstant(name="rgba4", description=""),
        EnumConstant(name="rgb5a1", description=""),
        EnumConstant(name="rgb565", description=""),
        EnumConstant(name="rgb10a2", description=""),
        EnumConstant(name="rg11b10f", description=""),
    ]
)

IMAGE_IMAGE_DATA_TYPE = Type(
    name="ImageData",
    description="ImageData object.",
    constructors=[],
    functions=[
        Function(name="getWidth", description="Method getWidth.", variants=[]),
        Function(name="getHeight", description="Method getHeight.", variants=[]),
        Function(name="getDimensions", description="Method getDimensions.", variants=[]),
        Function(name="getFormat", description="Method getFormat.", variants=[]),
        Function(name="setPixel", description="Method setPixel.", variants=[]),
        Function(name="getPixel", description="Method getPixel.", variants=[]),
        Function(name="paste", description="Method paste.", variants=[]),
        Function(name="encode", description="Method encode.", variants=[]),
    ],
    supertypes=["Object"]
)

IMAGE_COMPRESSED_IMAGE_DATA_TYPE = Type(
    name="CompressedImageData",
    description="CompressedImageData object.",
    constructors=[],
    functions=[
        Function(name="getWidth", description="Method getWidth.", variants=[]),
        Function(name="getHeight", description="Method getHeight.", variants=[]),
        Function(name="getDimensions", description="Method getDimensions.", variants=[]),
        Function(name="getFormat", description="Method getFormat.", variants=[]),
        Function(name="getMipmapCount", description="Method getMipmapCount.", variants=[]),
    ],
    supertypes=["Object"]
)

IMAGE_MODULE = Module(
    name="image",
    description="Provides image data types.",
    types=[
        IMAGE_IMAGE_DATA_TYPE,
        IMAGE_COMPRESSED_IMAGE_DATA_TYPE,
    ],
    functions=[],
    enums=[
        IMAGE_PIXEL_FORMAT_ENUM,
    ]
)

SOUND_SOUND_DATA_TYPE = Type(
    name="SoundData",
    description="SoundData object.",
    constructors=[],
    functions=[
        Function(name="getSample", description="Method getSample.", variants=[]),
        Function(name="setSample", description="Method setSample.", variants=[]),
        Function(name="getSampleRate", description="Method getSampleRate.", variants=[]),
        Function(name="getBitDepth", description="Method getBitDepth.", variants=[]),
        Function(name="getChannelCount", description="Method getChannelCount.", variants=[]),
        Function(name="getDuration", description="Method getDuration.", variants=[]),
    ],
    supertypes=["Object"]
)

SOUND_MODULE = Module(
    name="sound",
    description="Provides sound data types.",
    types=[
        SOUND_SOUND_DATA_TYPE,
    ],
    functions=[],
    enums=[]
)

DATA_COMPRESSED_DATA_TYPE = Type(
    name="CompressedData",
    description="CompressedData object.",
    constructors=[],
    functions=[
        Function(name="getFormat", description="Method getFormat.", variants=[]),
        Function(name="decompress", description="Method decompress.", variants=[]),
    ],
    supertypes=["Object"]
)

DATA_MODULE = Module(
    name="data",
    description="Provides data container types.",
    types=[
        DATA_COMPRESSED_DATA_TYPE,
    ],
    functions=[],
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
        JOYSTICK_MODULE,
        TIMER_MODULE,
        WINDOW_MODULE,
        EVENT_MODULE,
        FILESYSTEM_MODULE,
        AUDIO_MODULE,
        MATH_MODULE,
        TOUCH_MODULE,
        DATA_MODULE,
        IMAGE_MODULE,
        SOUND_MODULE,
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
