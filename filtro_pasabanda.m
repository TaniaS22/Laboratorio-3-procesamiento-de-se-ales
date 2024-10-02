% Asegúrate de tener la Toolbox Simbólica instalada
% Limpiar el entorno de trabajo
clear; clc; close all;

% Paso 1: Definir la variable simbólica
syms s

% Paso 2: Definir la función de transferencia original H(s)
H_original = 1 / ((s^2 + 0.76536*s + 1) * (s^2 + 1.84776*s + 1));

% Paso 3: Definir la sustitución de s
s_subs = (s^2 + 177647.4) / (2764.6 * s);

% Paso 4: Realizar la sustitución en H(s)
H_substituted = subs(H_original, s, s_subs);

% Paso 5: Simplificar la expresión resultante
H_simplified = simplify(H_substituted);

% Paso 6: Expandir el numerador y denominador para obtener polinomios
[num_sym, den_sym] = numden(H_simplified);
num_expanded = expand(num_sym);
den_expanded = expand(den_sym);

% Paso 7: Convertir los polinomios simbólicos a vectores de coeficientes
% Utilizar 'sym2poly' para convertir polinomios simbólicos a vectores numéricos
num_coeffs = double(sym2poly(num_expanded));
den_coeffs = double(sym2poly(den_expanded));

% Paso 8: Crear la función de transferencia utilizando 'tf'
H_transformed = tf(num_coeffs, den_coeffs);

% Mostrar la función de transferencia simplificada
disp('Función de transferencia después de la sustitución y simplificación:');
disp(H_transformed);

% Paso 9: Normalizar la función de transferencia para tener un punto de corte de 3 dB
% Obtener la magnitud y frecuencia de la función de transferencia
[mag, ~, w] = bode(H_transformed);
mag = squeeze(mag);  % Eliminar dimensiones singleton
w = squeeze(w);

% Encontrar el índice de la frecuencia donde la magnitud es máxima
[mag_max, idx_max] = max(mag);

% Calcular la magnitud en el punto de corte de 3 dB (1/sqrt(2) de la máxima)
mag_3dB = mag_max / sqrt(2);

% Encontrar la frecuencia más cercana a donde la magnitud es igual a mag_3dB
[~, idx_3dB] = min(abs(mag - mag_3dB));
w_3dB = w(idx_3dB);

% Calcular el valor de la ganancia en la frecuencia de corte
gain_3dB = mag(idx_3dB);

% Normalizar la función de transferencia
H_normalized = H_transformed / gain_3dB;

% Paso 10: Generar el Diagrama de Bode de la función de transferencia normalizada
figure;
bode(H_normalized);
grid on;
title('Diagrama de Bode de la Función de Transferencia Normalizada con 3 dB de Corte');

% Opcional: Mostrar información adicional
fprintf('Frecuencia de corte (rad/s): %.4f\n', w_3dB);
fprintf('Ganancia en frecuencia de corte antes de normalizar: %.4f\n', gain_3dB);
