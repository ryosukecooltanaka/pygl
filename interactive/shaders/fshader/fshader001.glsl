#version 410

uniform sampler2D Texture;

in vec2 v_text;
out vec3 color;

uniform vec3 fog_color;
uniform float fog_alpha;
uniform float fog_beta;

void main() {
   color = texture(Texture, v_text).rgb;
}
