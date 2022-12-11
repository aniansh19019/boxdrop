 % Part 1

 % Functions

function [q1_d, q2_d] = q_d(t)
%UNTITLED3 Summary of this function goes here
%   Detailed explanation goes here
q1_d = pi/3 + (pi/6)*sin(t);
q2_d = pi/4 + (pi/6)*cos(t);
end

function [q1_d_dot, q2_d_dot] = q_d_dot(t)
%UNTITLED4 Summary of this function goes here
%   Detailed explanation goes here
q1_d_dot = (pi/6)*cos(t); 
q2_d_dot = -(pi/6)*sin(t);
end
% this is a test comment

function Xdot = qdoubledot(t,X)

    % Part 1
    
    q = X(1:2, 1); % Angles
    q_dot = X(3:4, 1); % Angular Velocities

    % Model Parameters:
    
    
    m1 = 3.473;
    m2 = 0.196;
    a1 = 1;
    a2 = 1;
    f1 = 5.3;  
    f2 = 1.1; 

    g = -9.8;

    % PD controller coefficients

    Kp = 100;
    Kd = 20;

    % Desired Trajectory    

    [theta1_d, theta2_d] = q_d(t);
  
    [theta1_d_dot, theta2_d_dot] = q_d_dot(t);
    
    theta1_error = q(1) - theta1_d;
    theta2_error = q(2) - theta2_d;

    theta1_dot_error = q_dot(1) - theta1_d_dot;
    theta2_dot_error = q_dot(2) - theta2_d_dot;

    X_dot_error = [theta1_error;theta2_error;theta1_dot_error;theta2_dot_error];
    
    % Model Equations

    M = [(m1+m2)*a1^2+m2*a2^2+2*m2*a1*a2*cos(q(2)) m2*a2^2+m2*a1*a2*cos(q(2)); m2*a2^2+m2*a1*a2*cos(q(2)) m2*a2^2 ];
    V = [(-m2)*a1*a2*(2*q_dot(1)*q_dot(2)+q_dot(2)^2)*sin(q(2)); m2*(a1*a2*q(1)^2)*sin(q(2))];
    F = [f1 0; 0 f2];
    G = [(m1+m2)*g*a1*cos(q(1))+m2*g*a2*cos(q(1)+q(2)); m2*g*a2*cos(q(1)+q(2))];
    
    % Control Input
    
    q_errors= X_dot_error([1,2],1);
    q_dot_errors = X_dot_error([3,4],1);

    U = -Kp.*q_errors - Kd.*q_dot_errors;
    T = M*U+V +F*q_dot-G;

    
    % Compute q_double_dot
    Xdot = [q_dot;(inv(M))*(T-V-F*q_dot-G)];

end

% Plotting

[t,y] = ode45(@qdoubledot, [0 30],[0; 0; 0; 0]);

theta1= y(:,1);
theta2 = y(:,2);
theta1_dot = y(:,3);
theta2_dot = y(:,4);
time = t;

[theta1_d, theta2_d] = q_d(t)
[theta1_d_dot, theta2_d_dot] = q_d_dot(t)

error1 = theta1 - theta1_d;
error2 = theta2 - theta2_d;

error1_dot = theta1_dot - theta1_d_dot;
error2_dot = theta2_dot - theta2_d_dot;



tiledlayout(3,2)


nexttile
plot(t,error1)
title('Theta 1 Error')


nexttile
plot(t,error2)
title('Theta 2 Error')

nexttile
plot(t, error1_dot)
title('Theta 1 Dot Error')

nexttile
plot(t, error2_dot)
title('Theta 2 Dot Error')





% Part 2


function Xdot = qdoubledot(t,X)

    % Part 1
    
    q = X(1:2, 1); % Angles
    q_dot = X(3:4, 1); % Angular Velocities

    % Model Parameters:
    
    
    m1 = 3.473;
    m2 = 0.196;
    a1 = 1;
    a2 = 1;
    f1 = 5.3;  
    f2 = 1.1; 

    g = -9.8;

    % PD controller coefficients

    Kp = 100;
    Kd = 20;

    % Desired Trajectory    

    [theta1_d, theta2_d] = q_d(t);
  
    [theta1_d_dot, theta2_d_dot] = q_d_dot(t);
    
    theta1_error = q(1) - theta1_d;
    theta2_error = q(2) - theta2_d;

    theta1_dot_error = q_dot(1) - theta1_d_dot;
    theta2_dot_error = q_dot(2) - theta2_d_dot;

    X_dot_error = [theta1_error;theta2_error;theta1_dot_error;theta2_dot_error];
    
    % Model Equations

    M = [(m1+m2)*a1^2+m2*a2^2+2*m2*a1*a2*cos(q(2)) m2*a2^2+m2*a1*a2*cos(q(2)); m2*a2^2+m2*a1*a2*cos(q(2)) m2*a2^2 ];
    V = [(-m2)*a1*a2*(2*q_dot(1)*q_dot(2)+q_dot(2)^2)*sin(q(2)); m2*(a1*a2*q(1)^2)*sin(q(2))];
    F = [f1 0; 0 f2];
    G = [(m1+m2)*g*a1*cos(q(1))+m2*g*a2*cos(q(1)+q(2)); m2*g*a2*cos(q(1)+q(2))];
    
    % Control Input
    
    q_errors= X_dot_error([1,2],1);
    q_dot_errors = X_dot_error([3,4],1);

    T = -Kp.*q_errors - Kd.*q_dot_errors;

    
    % Compute q_double_dot
    Xdot = [q_dot;(inv(M))*(T-V-F*q_dot-G)];

end


% Plotting

[t,y] = ode45(@qdoubledot, [0 30],[0; 0; 0; 0]);

theta1= y(:,1);
theta2 = y(:,2);
theta1_dot = y(:,3);
theta2_dot = y(:,4);
time = t;

[theta1_d, theta2_d] = q_d(t)
[theta1_d_dot, theta2_d_dot] = q_d_dot(t)

error1 = theta1 - theta1_d;
error2 = theta2 - theta2_d;

error1_dot = theta1_dot - theta1_d_dot;
error2_dot = theta2_dot - theta2_d_dot;



tiledlayout(3,2)


nexttile
plot(t,error1)
title('Theta 1 Error')


nexttile
plot(t,error2)
title('Theta 2 Error')

nexttile
plot(t, error1_dot)
title('Theta 1 Dot Error')

nexttile
plot(t, error2_dot)
title('Theta 1 Dot Error')


 % Part 1

 % Functions

function [q1_d, q2_d] = q_d(t)
%UNTITLED3 Summary of this function goes here
%   Detailed explanation goes here
q1_d = pi/3 + (pi/6)*sin(t);
q2_d = pi/4 + (pi/6)*cos(t);
end

function [q1_d_dot, q2_d_dot] = q_d_dot(t)
%UNTITLED4 Summary of this function goes here
%   Detailed explanation goes here
q1_d_dot = (pi/6)*cos(t); 
q2_d_dot = -(pi/6)*sin(t);
end
% this is a test comment

function Xdot = qdoubledot(t,X)

    % Part 1
    
    q = X(1:2, 1); % Angles
    q_dot = X(3:4, 1); % Angular Velocities

    % Model Parameters:
    
    
    m1 = 3.473;
    m2 = 0.196;
    a1 = 1;
    a2 = 1;
    f1 = 5.3;  
    f2 = 1.1; 

    g = -9.8;

    % PD controller coefficients

    Kp = 100;
    Kd = 20;

    % Desired Trajectory    

    [theta1_d, theta2_d] = q_d(t);
  
    [theta1_d_dot, theta2_d_dot] = q_d_dot(t);
    
    theta1_error = q(1) - theta1_d;
    theta2_error = q(2) - theta2_d;

    theta1_dot_error = q_dot(1) - theta1_d_dot;
    theta2_dot_error = q_dot(2) - theta2_d_dot;

    X_dot_error = [theta1_error;theta2_error;theta1_dot_error;theta2_dot_error];
    
    % Model Equations

    M = [(m1+m2)*a1^2+m2*a2^2+2*m2*a1*a2*cos(q(2)) m2*a2^2+m2*a1*a2*cos(q(2)); m2*a2^2+m2*a1*a2*cos(q(2)) m2*a2^2 ];
    V = [(-m2)*a1*a2*(2*q_dot(1)*q_dot(2)+q_dot(2)^2)*sin(q(2)); m2*(a1*a2*q(1)^2)*sin(q(2))];
    F = [f1 0; 0 f2];
    G = [(m1+m2)*g*a1*cos(q(1))+m2*g*a2*cos(q(1)+q(2)); m2*g*a2*cos(q(1)+q(2))];
    
    % Control Input
    
    q_errors= X_dot_error([1,2],1);
    q_dot_errors = X_dot_error([3,4],1);

    U = -Kp.*q_errors - Kd.*q_dot_errors;
    T = M*U+V +F*q_dot-G;

    
    % Compute q_double_dot
    Xdot = [q_dot;(inv(M))*(T-V-F*q_dot-G)];

end

% Plotting

[t,y] = ode45(@qdoubledot, [0 30],[0; 0; 0; 0]);

theta1= y(:,1);
theta2 = y(:,2);
theta1_dot = y(:,3);
theta2_dot = y(:,4);
time = t;

[theta1_d, theta2_d] = q_d(t)
[theta1_d_dot, theta2_d_dot] = q_d_dot(t)

error1 = theta1 - theta1_d;
error2 = theta2 - theta2_d;

error1_dot = theta1_dot - theta1_d_dot;
error2_dot = theta2_dot - theta2_d_dot;



tiledlayout(3,2)


nexttile
plot(t,error1)
title('Theta 1 Error')


nexttile
plot(t,error2)
title('Theta 2 Error')

nexttile
plot(t, error1_dot)
title('Theta 1 Dot Error')

nexttile
plot(t, error2_dot)
title('Theta 2 Dot Error')





% Part 2


function Xdot = qdoubledot(t,X)

    % Part 1
    
    q = X(1:2, 1); % Angles
    q_dot = X(3:4, 1); % Angular Velocities

    % Model Parameters:
    
    
    m1 = 3.473;
    m2 = 0.196;
    a1 = 1;
    a2 = 1;
    f1 = 5.3;  
    f2 = 1.1; 

    g = -9.8;

    % PD controller coefficients

    Kp = 100;
    Kd = 20;

    % Desired Trajectory    

    [theta1_d, theta2_d] = q_d(t);
  
    [theta1_d_dot, theta2_d_dot] = q_d_dot(t);
    
    theta1_error = q(1) - theta1_d;
    theta2_error = q(2) - theta2_d;

    theta1_dot_error = q_dot(1) - theta1_d_dot;
    theta2_dot_error = q_dot(2) - theta2_d_dot;

    X_dot_error = [theta1_error;theta2_error;theta1_dot_error;theta2_dot_error];
    
    % Model Equations

    M = [(m1+m2)*a1^2+m2*a2^2+2*m2*a1*a2*cos(q(2)) m2*a2^2+m2*a1*a2*cos(q(2)); m2*a2^2+m2*a1*a2*cos(q(2)) m2*a2^2 ];
    V = [(-m2)*a1*a2*(2*q_dot(1)*q_dot(2)+q_dot(2)^2)*sin(q(2)); m2*(a1*a2*q(1)^2)*sin(q(2))];
    F = [f1 0; 0 f2];
    G = [(m1+m2)*g*a1*cos(q(1))+m2*g*a2*cos(q(1)+q(2)); m2*g*a2*cos(q(1)+q(2))];
    
    % Control Input
    
    q_errors= X_dot_error([1,2],1);
    q_dot_errors = X_dot_error([3,4],1);

    T = -Kp.*q_errors - Kd.*q_dot_errors;

    
    % Compute q_double_dot
    Xdot = [q_dot;(inv(M))*(T-V-F*q_dot-G)];

end


% Plotting

[t,y] = ode45(@qdoubledot, [0 30],[0; 0; 0; 0]);

theta1= y(:,1);
theta2 = y(:,2);
theta1_dot = y(:,3);
theta2_dot = y(:,4);
time = t;

[theta1_d, theta2_d] = q_d(t)
[theta1_d_dot, theta2_d_dot] = q_d_dot(t)

error1 = theta1 - theta1_d;
error2 = theta2 - theta2_d;

error1_dot = theta1_dot - theta1_d_dot;
error2_dot = theta2_dot - theta2_d_dot;



tiledlayout(3,2)


nexttile
plot(t,error1)
title('Theta 1 Error')


nexttile
plot(t,error2)
title('Theta 2 Error')

nexttile
plot(t, error1_dot)
title('Theta 1 Dot Error')

nexttile
plot(t, error2_dot)
title('Theta 1 Dot Error')


