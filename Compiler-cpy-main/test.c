int main()
{
	int x,y,z,m,m2,counterFunctionCalls,x,counterFunctionCalls,x,i,x,y,counterFunctionCalls,counterFunctionCalls,x,y,x,counterFunctionCalls,counterFunctionCalls,year,counterFunctionCalls;

	L_1: T_1 = counterFunctionCalls+1;

	L_2: counterFunctionCalls = T_1;

	L_3: if (x>y) goto L__;

	L_4: goto L_6;

	L_5: if (x>z) goto L_8;

	L_6: goto L_10;

	L_7: m = x;

	L_8: goto L_18;

	L_9: if (y>x) goto L__;

	L_10: goto L_12;

	L_11: if (y>z) goto L_14;

	L_12: goto L_16;

	L_13: m = y;

	L_14: goto L_16;

	L_15: m = z;

	L_16: return(m);

	L_19: T_2 = counterFunctionCalls+1;

	L_20: counterFunctionCalls = T_2;

	L_21: if (x<0) goto L_24;

	L_22: goto L_26;

	L_23: return(1);

	L_24: goto L_40;

	L_25: if (x=0) goto L_30;

	L_26: goto L_28;

	L_27: if (x=1) goto L_30;

	L_28: goto L_32;

	L_29: return(1);

	L_30: goto L_32;

	L_31: T_3 = x-1;

	L_33: {};

	L_34: T_5 = x-2;

	L_36: {};

	L_37: T_7 = T_4+T_6;

	L_38: return(T_7);

	L_41: T_8 = counterFunctionCalls+1;

	L_42: counterFunctionCalls = T_8;

	L_43: if (y//x) goto L_T_9;

	L_44: T_10 = T_9*x;

	L_45: if (y=T_10) goto L_48;

	L_46: goto L_50;

	L_47: return(1);

	L_48: goto L_51;

	L_49: return(0);

	L_52: T_11 = counterFunctionCalls+1;

	L_53: counterFunctionCalls = T_11;

	L_54: i = 2;

	L_55: if (i<x) goto L_58;

	L_56: goto L_67;

	L_58: {};

	L_59: if (T_12=1) goto L_62;

	L_60: goto L_66;

	L_61: return(0);

	L_62: T_13 = i+1;

	L_63: i = T_13;

	L_64: goto L_66;

	L_65: goto L_56;

	L_66: return(1);

	L_69: T_14 = counterFunctionCalls+1;

	L_70: counterFunctionCalls = T_14;

	L_71: T_15 = x*x;

	L_72: return(T_15);

	L_75: T_16 = counterFunctionCalls+1;

	L_76: counterFunctionCalls = T_16;

	L_78: {};

	L_80: {};

	L_81: T_19 = T_17*T_18;

	L_82: y = T_19;

	L_83: return(y);

	L_86: T_20 = counterFunctionCalls+1;

	L_87: counterFunctionCalls = T_20;

	L_88: if (year%4) goto L_T_21;

	L_89: if (T_21=0) goto L__;

	L_90: goto L_92;

	L_91: if (year%100) goto L_T_22;

	L_92: if (T_22!=0) goto L_98;

	L_93: goto L_95;

	L_94: if (year%400) goto L_T_23;

	L_95: if (T_23=0) goto L_98;

	L_96: goto L_100;

	L_97: return(1);

	L_98: goto L_101;

	L_99: return(0);

	L_102: counterFunctionCalls = 0;

	L_103: i = input;

	L_104: print("%d",i);

	L_105: i = 1600;

	L_106: if (i<=2000) goto L_109;

	L_107: goto L_115;

	L_109: {};

	L_110: print("%d",T_24);

	L_111: T_25 = i+400;

	L_112: i = T_25;

	L_113: goto L_107;

	L_115: {};

	L_116: print("%d",T_26);

	L_118: {};

	L_119: print("%d",T_27);

	L_121: {};

	L_122: print("%d",T_28);

	L_124: {};

	L_125: print("%d",T_29);

	L_126: i = 1;

	L_127: if (i<=12) goto L_130;

	L_128: goto L_136;

	L_130: {};

	L_131: print("%d",T_30);

	L_132: T_31 = i+1;

	L_133: i = T_31;

	L_134: goto L_128;

	L_135: print("%d",counterFunctionCalls);

	L_136: {};
}