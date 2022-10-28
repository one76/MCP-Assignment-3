%pg. 508-510 UM
%serial prac

baud_target = 115200;
pclk = 60e6;      % ? MHz   CPU clock divisor: 2

% table 406 values
load('FR_DIV_MUL.mat');
FR = FR_DIV_MUL(:,1);
DIV = FR_DIV_MUL(:,2);
MUL =  FR_DIV_MUL(:,3);

%flow chart step 1 - check for an integer
DL_est_check = sum(isinteger((pclk ./  (16 * baud_target))));

%flow chart step 2 - if not integer guess 1.5
FR_est_0 = 1.5;
DL_est = round((pclk /  (16 * baud_target * FR_est_0)));
FR_est = (pclk /  (16 * baud_target * DL_est));

%flow chart step 3 - find closest value in table
[val,idx] = min(abs(FR - FR_est));
DIVADDVAL = DIV(idx);
MULVAL = MUL(idx);

% flow chart step 4 - use DL_est to fill LSB and MSB of DL
% DLL = ;
% DLM = ;

% check the baud rate
baud_actual = pclk / (16 * (256 * DLM + DLL )*(1+DIVADDVAL/MULVAL))

% deviation of baud rate to target
actual_rel_target = baud_actual/baud_target