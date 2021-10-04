#version 330
in layout(location =  0) vec3 position;
in layout(location =  1) vec3 color;
in layout(location =  3) vec3 vertNormal;
in layout(location = 10) vec3 aPos;

// shader select
uniform int selector;

// object
uniform mat4 view;
uniform mat4 model;
uniform mat4 projection;

// ui
uniform mat4 ortho;
uniform mat4 orthoView;

// sky
out vec3 TexCoords;


out vec3 lightColor;
out vec3 FragPos;
out vec3 Normal;

out VS_OUT {
    vec3 normal;
} vs_out;

void shading_obj() {
    lightColor  = color;
    FragPos = vec3(model * vec4(position, 1.0));
    Normal = (model * vec4(vertNormal, 0.0f)).xyz;
    gl_Position = projection * view * model * vec4(position, 1.0f);

    //mat3 normalMatrix = mat3(transpose(inverse(view * model)));
    //vs_out.normal = normalize(vec3(projection * vec4(normalMatrix * vertNormal, 0.0)));
    //lightColor  = color;
    //FragPos = vec3(model * vec4(position, 1.0));
    //FragPos = vec3(model * vec4(position, 1.0));
    //Normal = mat3(transpose(inverse(model))) * vertNormal; 
    //Normal = vertNormal;
    //Normal = (light * vec4(vertNormal, 0.0f)).xyz;
    //Normal = mat3(transpose(inverse(model))) * vertNormal
    //gl_Position = projection * view * model * vec4(position, 1.0f);
}

void shading_ui() {
    lightColor  = color;
    gl_Position = ( 
        ortho * orthoView * vec4(position, 1.0f)
    );
}

void shading_skybox() {
    //#version 330 core
    //layout (location = 0) in vec3 aPos;
    //
    //out vec3 TexCoords;
    //
    //uniform mat4 projection;
    //uniform mat4 view;
    //
    //void main()
    //{
    //    TexCoords = aPos;
    //    vec4 pos = projection * view * vec4(aPos, 1.0);
    //    gl_Position = pos.xyzw;
    //}
    TexCoords = aPos;
    vec4 pos = projection * view * vec4(aPos, 1.0);
    gl_Position = pos.xyww;
}

void main() {
    // OBJECT rendering
    if (selector==1) { shading_obj(); }
    // SKYBOX rendering
    else if (selector==2) { shading_skybox(); }
    // UI rendering
    else { shading_ui(); }
}