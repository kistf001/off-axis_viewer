#version 330
out vec4 FragColor;

struct Material {
    vec3 ambient;
    vec3 diffuse;
    vec3 specular;    
    int shininess;
}; 
struct Light {
    vec3 position;
    vec3 direction;

    vec3 ambient;
    vec3 diffuse;
    vec3 specular;
	
    float constant;
    float linear;
    float quadratic;
};

in vec3 lightColor ;
in vec3 FragPos;  
in vec3 Normal;
in vec3 TexCoords;

uniform vec3 view;
uniform int selector;
uniform Material material;
uniform Light light;
uniform samplerCube skybox;

void shading_obj(){

    vec3 directionsss = vec3(-1.0f, -1.0f, -1.0f);

    // ambient
    vec3 ambient = light.ambient * material.ambient;

    // diffuse 
    vec3 norm = normalize(Normal);
    vec3 lightDir = normalize(light.position - FragPos);
    float diff = max(dot(norm, lightDir), 0.0f);
    vec3 diffuse = light.diffuse * (diff * material.diffuse);

    // specular
    vec3 viewDir = normalize(vec3(0.0f, 0.0f, 100f) - FragPos);
    vec3 reflectDir = reflect(-lightDir, norm);  
    float spec = pow(max(dot(viewDir, reflectDir), 0.0), material.shininess);
    vec3 specular = light.specular * (spec * material.specular) ; 
    
    vec3 lightIntensity;
    lightIntensity += ambient;
    lightIntensity += diffuse;
    lightIntensity += specular;

    //FragColor = vec4((normalize(Normal)/2)+0.5, 1.0f);
    //FragColor = vec4(lightIntensity, 1.0f);

    
    vec3 I = normalize(lightDir);
    vec3 R = reflect(I, normalize(Normal));
    FragColor = vec4(texture(skybox, R).rgb*lightIntensity, 1.0);
    
    //float gamma = 2.2;
    //FragColor = vec4(pow(texture(skybox, R).rgb*lightIntensity, vec3(1.0/gamma)), 1.0);
    
    //FragColor = vec4(1.0, 0.0, 0.0, 1.0);

}

void shading_skybox() {
    //#version 330 core
    //out vec4 FragColor;

    //in vec3 TexCoords;

    //uniform samplerCube skybox;

    //void main()
    //{    
    //    FragColor = texture(skybox, TexCoords);
    //}
    FragColor = texture(skybox, TexCoords);
}

void shading_ui() { 
    FragColor = vec4(lightColor , 1.0f); 
}

void main() {
    // OBJECT rendering
    if (selector==1) { shading_obj(); }
    else if (selector==2) { shading_skybox(); }
    // UI rendering
    else { shading_ui(); }
}
