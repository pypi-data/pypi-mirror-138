//this file is autogenerated using stringify.bat (premake --stringify) in the build folder of this project
static const char* projectiveTextureInstancingFragmentShader= \
"#version 330 core\n"
"//precision highp float;\n"
"in Fragment\n"
"{\n"
"     vec4 color;\n"
"} fragment;\n"
"uniform sampler2D Diffuse;\n"
"uniform mat4 ViewMatrixInverse;\n"
"uniform mat4 TextureMVP;\n"
"in vec3 lightPos,cameraPosition, normal,ambient;\n"
"in vec4 vertexPos;\n"
"in float materialShininess;\n"
"in vec3 lightSpecularIntensity;\n"
"in vec3 materialSpecularColor;\n"
"out vec4 color;\n"
"void main(void)\n"
"{\n"
"    vec4 projcoords = TextureMVP * vertexPos;\n"
"    vec2 texturecoords = projcoords.xy/projcoords.w;\n"
"	vec4 texel = fragment.color*texture(Diffuse,texturecoords);\n"
"	vec3 ct,cf;\n"
"	float intensity,at,af;\n"
"	if (fragment.color.w==0)\n"
"		discard;\n"
"	vec3 lightDir = normalize(lightPos);\n"
"	\n"
"	vec3 normalDir = normalize(normal);\n"
" \n"
"	intensity = 0.5+0.5*clamp( dot( normalDir,lightDir ), -1,1 );\n"
"	\n"
"	af = 1.0;\n"
"		\n"
"	ct = texel.rgb;\n"
"	at = texel.a;\n"
"		\n"
"	//float bias = 0.005f;\n"
"	\n"
"	vec3 specularReflection;\n"
"	\n"
"	if (dot(normalDir, lightDir) < 0.0) \n"
"	{\n"
"		specularReflection = vec3(0.0, 0.0, 0.0);\n"
"	}\n"
"  else // light source on the right side\n"
"	{\n"
"		vec3 surfaceToLight = normalize(lightPos - vertexPos.xyz);\n"
"    vec3 surfaceToCamera = normalize(cameraPosition - vertexPos.xyz);\n"
"    \n"
"    \n"
"    float specularCoefficient = 0.0;\n"
"		specularCoefficient = pow(max(0.0, dot(surfaceToCamera, reflect(-surfaceToLight, normalDir))), materialShininess);\n"
"    specularReflection = specularCoefficient * materialSpecularColor * lightSpecularIntensity;\n"
"  \n"
"	}\n"
"    \n"
"	float visibility = 1.0;\n"
"	intensity = 0.7*intensity  + 0.3*intensity*visibility;\n"
"	\n"
"	cf = intensity*(vec3(1.0,1.0,1.0)-ambient)+ambient+specularReflection*visibility;\n"
"	color  = vec4(ct * cf, fragment.color.w);\n"
"}\n"
;
