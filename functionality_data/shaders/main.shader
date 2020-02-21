name: main
shaders:
    vertex: |
        #version 330 core

        layout (location = 0) in vec3 in_Pos;
        layout (location = 1) in vec3 in_Norm;
        layout (location = 2) in vec2 in_UV;
        layout (location = 3) in vec4 in_Color;

        uniform mat4 ViewMatrix;
        uniform mat4 ProjectionMatrix;

        void main()
        {
            gl_Position = ProjectionMatrix * ViewMatrix * vec4(in_Pos, 1.0);
        }
    fragment: |
        #version 330 core

        out vec4 out_FragColor;

        void main()
        {
            out_FragColor = vec4(0, 1, 1, 1);
        }
