//Maya ASCII 2017ff05 scene
//Name: omtk.matrixFrom2Vectors_v0.0.1.ma
//Last modified: Thu, Oct 31, 2019 09:56:45 PM
//Codeset: UTF-8
requires maya "2017ff05";
requires "stereoCamera" "10.0";
requires "redshift4maya" "2.0.93";
requires "mgNurbsSurfShaper.py" "1.0";
requires "mglLockSet" "2013.0";
requires "mgDispDeformer" "1.0";
requires "mgRayIntersect" "1.1";
requires "MayaKrakatoa" "1.0";
requires "stereoCamera" "10.0";
requires "AmatShader" "1.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2017";
fileInfo "version" "2017";
fileInfo "cutIdentifier" "201710312130-1018716";
fileInfo "osv" "Linux 4.18.0-20-generic #21~18.04.1pop0-Ubuntu SMP Wed May 15 14:41:28 UTC 2019 x86_64";
fileInfo "omtk.compound.author" "Renaud Lessard Larouche";
fileInfo "omtk.compound.version" "0.0.1";
fileInfo "omtk.compound.uid" "7bfec70f-a117-4c4f-841d-2c349ed1d0ef";
fileInfo "omtk.compound.name" "omtk.matrixFrom2Vectors";
createNode vectorProduct -n "getEye";
	rename -uid "944B3980-0000-407A-5C99-8B5800000794";
	setAttr ".op" 2;
createNode fourByFourMatrix -n "getMatrix";
	rename -uid "944B3980-0000-407A-5C99-8B580000079A";
createNode vectorProduct -n "getUp";
	rename -uid "944B3980-0000-407A-5C99-8B5800000795";
	setAttr ".op" 2;
createNode network -n "inputs";
	rename -uid "944B3980-0000-407A-5C99-8B5800000797";
	addAttr -ci true -sn "pos1" -ln "pos1" -at "float3" -nc 3;
	addAttr -ci true -sn "pos1X" -ln "pos1X" -at "float" -p "pos1";
	addAttr -ci true -sn "pos1Y" -ln "pos1Y" -at "float" -p "pos1";
	addAttr -ci true -sn "pos1Z" -ln "pos1Z" -at "float" -p "pos1";
	addAttr -ci true -sn "pos2" -ln "pos2" -at "float3" -nc 3;
	addAttr -ci true -sn "pos2X" -ln "pos2X" -at "float" -p "pos2";
	addAttr -ci true -sn "pos2Y" -ln "pos2Y" -at "float" -p "pos2";
	addAttr -ci true -sn "pos2Z" -ln "pos2Z" -at "float" -p "pos2";
	addAttr -ci true -sn "pos" -ln "pos" -at "float3" -nc 3;
	addAttr -ci true -sn "posX" -ln "posX" -at "float" -p "pos";
	addAttr -ci true -sn "posY" -ln "posY" -at "float" -p "pos";
	addAttr -ci true -sn "posZ" -ln "posZ" -at "float" -p "pos";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr ".pos1" -type "float3" 0 -0.52542102 1.9638686 ;
	setAttr ".pos2" -type "float3" 0 1 0 ;
	setAttr ".pos" -type "float3" 0.82893044 0.71890557 0.40646583 ;
	setAttr ".nts" -type "string" "version:'0.0.1'\nuid:'7bfec70f-a117-4c4f-841d-2c349ed1d0ef'\nname:'omtk.matrixFrom2Vectors'\nauthor:'Renaud Lessard Larouche'";
createNode vectorProduct -n "normalizeLook";
	rename -uid "944B3980-0000-407A-5C99-8B5800000796";
	setAttr ".op" 0;
	setAttr ".no" yes;
createNode vectorProduct -n "normalizeUp";
	rename -uid "944B3980-0000-407A-5C99-8B580000079B";
	setAttr ".op" 0;
	setAttr ".no" yes;
createNode network -n "outputs";
	rename -uid "944B3980-0000-407A-5C99-8B5800000798";
	addAttr -ci true -sn "outputMatrix" -ln "outputMatrix" -at "matrix";
	addAttr -ci true -sn "lookAxis" -ln "lookAxis" -at "float3" -nc 3;
	addAttr -ci true -sn "lookAxisX" -ln "lookAxisX" -at "float" -p "lookAxis";
	addAttr -ci true -sn "lookAxisY" -ln "lookAxisY" -at "float" -p "lookAxis";
	addAttr -ci true -sn "lookAxisZ" -ln "lookAxisZ" -at "float" -p "lookAxis";
	addAttr -ci true -sn "upAxis" -ln "upAxis" -at "float3" -nc 3;
	addAttr -ci true -sn "upAxisX" -ln "upAxisX" -at "float" -p "upAxis";
	addAttr -ci true -sn "upAxisY" -ln "upAxisY" -at "float" -p "upAxis";
	addAttr -ci true -sn "upAxisZ" -ln "upAxisZ" -at "float" -p "upAxis";
	addAttr -ci true -sn "eyeAxis" -ln "eyeAxis" -at "float3" -nc 3;
	addAttr -ci true -sn "eyeAxisX" -ln "eyeAxisX" -at "float" -p "eyeAxis";
	addAttr -ci true -sn "eyeAxisY" -ln "eyeAxisY" -at "float" -p "eyeAxis";
	addAttr -ci true -sn "eyeAxisZ" -ln "eyeAxisZ" -at "float" -p "eyeAxis";
select -ne :time1;
	setAttr -av -k on ".cch";
	setAttr -av -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".o" 0;
	setAttr -av ".unw";
	setAttr -k on ".etw";
	setAttr -k on ".tps";
	setAttr -k on ".tms";
select -ne :hardwareRenderingGlobals;
	setAttr ".otfna" -type "stringArray" 22 "NURBS Curves" "NURBS Surfaces" "Polygons" "Subdiv Surface" "Particles" "Particle Instance" "Fluids" "Strokes" "Image Planes" "UI" "Lights" "Cameras" "Locators" "Joints" "IK Handles" "Deformers" "Motion Trails" "Components" "Hair Systems" "Follicles" "Misc. UI" "Ornaments"  ;
	setAttr ".otfva" -type "Int32Array" 22 0 1 1 1 1 1
		 1 1 1 0 0 0 0 0 0 0 0 0
		 0 0 0 0 ;
select -ne :renderPartition;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 18 ".st";
	setAttr -cb on ".an";
	setAttr -cb on ".pt";
select -ne :renderGlobalsList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
select -ne :defaultShaderList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 20 ".s";
select -ne :postProcessList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".p";
select -ne :defaultRenderUtilityList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 36 ".u";
select -ne :defaultRenderingList1;
	setAttr -s 10 ".r";
select -ne :initialShadingGroup;
	setAttr -av -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".mwc";
	setAttr -cb on ".an";
	setAttr -cb on ".il";
	setAttr -cb on ".vo";
	setAttr -cb on ".eo";
	setAttr -cb on ".fo";
	setAttr -cb on ".epo";
	setAttr -k on ".ro" yes;
select -ne :initialParticleSE;
	setAttr -av -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".mwc";
	setAttr -k on ".an";
	setAttr -k on ".il";
	setAttr -k on ".vo";
	setAttr -k on ".eo";
	setAttr -k on ".fo";
	setAttr -k on ".epo";
	setAttr -k on ".ro" yes;
select -ne :defaultResolution;
	setAttr -av -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -k on ".bnm";
	setAttr -av -k on ".w";
	setAttr -av -k on ".h";
	setAttr -av -k on ".pa" 1;
	setAttr -av -k on ".al";
	setAttr -av -k on ".dar";
	setAttr -av -k on ".ldar";
	setAttr -cb on ".dpi";
	setAttr -av -k on ".off";
	setAttr -av -k on ".fld";
	setAttr -av -k on ".zsl";
	setAttr -cb on ".isu";
	setAttr -cb on ".pdu";
select -ne :defaultColorMgtGlobals;
	setAttr ".cme" no;
select -ne :hardwareRenderGlobals;
	setAttr -k on ".cch";
	setAttr -k on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k off ".ctrs" 256;
	setAttr -av -k off ".btrs" 512;
	setAttr -k off ".fbfm";
	setAttr -k off -cb on ".ehql";
	setAttr -k off -cb on ".eams";
	setAttr -k off -cb on ".eeaa";
	setAttr -k off -cb on ".engm";
	setAttr -k off -cb on ".mes";
	setAttr -k off -cb on ".emb";
	setAttr -av -k off -cb on ".mbbf";
	setAttr -k off -cb on ".mbs";
	setAttr -k off -cb on ".trm";
	setAttr -k off -cb on ".tshc";
	setAttr -k off ".enpt";
	setAttr -k off -cb on ".clmt";
	setAttr -k off -cb on ".tcov";
	setAttr -k off -cb on ".lith";
	setAttr -k off -cb on ".sobc";
	setAttr -k off -cb on ".cuth";
	setAttr -k off -cb on ".hgcd";
	setAttr -k off -cb on ".hgci";
	setAttr -k off -cb on ".mgcs";
	setAttr -k off -cb on ".twa";
	setAttr -k off -cb on ".twz";
	setAttr -k on ".hwcc";
	setAttr -k on ".hwdp";
	setAttr -k on ".hwql";
	setAttr -k on ".hwfr";
	setAttr -k on ".soll";
	setAttr -k on ".sosl";
	setAttr -k on ".bswa";
	setAttr -k on ".shml";
	setAttr -k on ".hwel";
connectAttr "normalizeLook.o" "getEye.i1"
		;
connectAttr "getUp.o" "getEye.i2"
		;
connectAttr "normalizeLook.ox" "getMatrix.i00"
		;
connectAttr "normalizeLook.oy" "getMatrix.i01"
		;
connectAttr "normalizeLook.oz" "getMatrix.i02"
		;
connectAttr "getUp.ox" "getMatrix.i10"
		;
connectAttr "getUp.oy" "getMatrix.i11"
		;
connectAttr "getUp.oz" "getMatrix.i12"
		;
connectAttr "getEye.ox" "getMatrix.i20"
		;
connectAttr "getEye.oy" "getMatrix.i21"
		;
connectAttr "getEye.oz" "getMatrix.i22"
		;
connectAttr "inputs.posY" "getMatrix.i31"
		;
connectAttr "inputs.posZ" "getMatrix.i32"
		;
connectAttr "inputs.posX" "getMatrix.i30"
		;
connectAttr "normalizeUp.o" "getUp.i1"
		;
connectAttr "normalizeLook.o" "getUp.i2"
		;
connectAttr "inputs.pos1" "normalizeLook.i1"
		;
connectAttr "inputs.pos2" "normalizeUp.i1"
		;
connectAttr "getMatrix.o" "outputs.outputMatrix"
		;
connectAttr "normalizeUp.o" "outputs.lookAxis"
		;
connectAttr "getUp.o" "outputs.upAxis"
		;
connectAttr "getEye.o" "outputs.eyeAxis"
		;
connectAttr "getMatrix.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "normalizeUp.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "normalizeLook.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "getUp.msg" ":defaultRenderUtilityList1.u"
		 -na;
connectAttr "getEye.msg" ":defaultRenderUtilityList1.u"
		 -na;
// End of omtk.matrixFrom2Vectors_v0.0.1.ma
