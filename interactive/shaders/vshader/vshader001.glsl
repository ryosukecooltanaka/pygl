#version 410

in vec3 xyz;
in vec2 uv;

out vec2 v_text;

uniform float z_near;
uniform float z_far;
uniform float fovx;
uniform float fovy;

uniform vec3 center;
uniform vec3 eye;
uniform vec3 up;

uniform vec3 rotations;
uniform vec3 translations;

mat4 perspective() {
    float zmul = (-2.0 * z_near * z_far) / (z_far - z_near);
    float xmul = 1.0 / tan(fovx);
    float ymul = 1.0 / tan(fovy);
    return mat4(
        xmul, 0.0, 0.0, 0.0,
        0.0, ymul, 0.0, 0.0,
        0.0, 0.0, -1.0, -1.0,
        0.0, 0.0, zmul, 0.0
    );
}

mat4 lookat() {
    vec3 forward = normalize(center - eye);
    vec3 side = normalize(cross(forward, up));
    vec3 upward = cross(side, forward);
    return mat4(
        side.x, upward.x, -forward.x, 0,
        side.y, upward.y, -forward.y, 0,
        side.z, upward.z, -forward.z, 0,
        -dot(eye, side), -dot(eye, upward), dot(eye, forward), 1
    );
}

mat3 aboutX() {
    return mat3(
        1, 0, 0,
        0, cos(rotations.x), sin(rotations.x),
        0, -sin(rotations.x), cos(rotations.x)
    );
}

mat3 aboutY() {
    return mat3(
        cos(rotations.y),  0, sin(rotations.y),
        0,                 1, 0,
        -sin(rotations.y), 0, cos(rotations.y)
    );
}

mat3 aboutZ() {
    return mat3(
        cos(rotations.z), sin(rotations.z), 0,
        -sin(rotations.z), cos(rotations.z), 0,
        0, 0, 1
    );
}

void main() {
    vec3 rotated = aboutZ() * aboutY() * aboutX() * xyz;
    vec3 translated = rotated + translations;
    vec4 lookedat = lookat() * vec4(translated, 1.0);
    gl_Position = perspective() * lookedat;
    v_text = uv;
}
