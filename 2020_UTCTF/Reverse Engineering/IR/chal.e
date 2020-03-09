
@check = dso_local global [64 x i8] c"\03\12\1A\17\0A\EC\F2\14\0E\05\03\1D\19\0E\02\0A\1F\07\0C\01\17\06\0C\0A\19\13\0A\16\1C\18\08\07\1A\03\1D\1C\11\0B\F3\87\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\00\05", align 16, !dbg !0
@MAX_SIZE = dso_local global i32 64, align 4, !dbg !8

define dso_local i32 @_Z7reversePc(i8*) #0 !dbg !19 {
  %2 = alloca i32, align 4
  %3 = alloca i8*, align 8
  %4 = alloca i32, align 4
  %5 = alloca i32, align 4
  %6 = alloca i32, align 4
  store i8* %0, i8** %3, align 8
  call void @llvm.dbg.declare(metadata i8** %3, metadata !24, metadata !DIExpression()), !dbg !25
  call void @llvm.dbg.declare(metadata i32* %4, metadata !26, metadata !DIExpression()), !dbg !28
  store i32 0, i32* %4, align 4, !dbg !28
  br label %7, !dbg !29

7:                                                ; preds = %20, %1
  %8 = load i32, i32* %4, align 4, !dbg !30
  %9 = load i32, i32* @MAX_SIZE, align 4, !dbg !32
  %10 = icmp slt i32 %8, %9, !dbg !33
  br i1 %10, label %11, label %23, !dbg !34

11:                                               ; preds = %7
  %12 = load i8*, i8** %3, align 8, !dbg !35
  %13 = load i32, i32* %4, align 4, !dbg !37
  %14 = sext i32 %13 to i64, !dbg !35
  %15 = getelementptr inbounds i8, i8* %12, i64 %14, !dbg !35
  %16 = load i8, i8* %15, align 1, !dbg !38
  %17 = sext i8 %16 to i32, !dbg !38
  %18 = add nsw i32 %17, 5, !dbg !38
  %19 = trunc i32 %18 to i8, !dbg !38
  store i8 %19, i8* %15, align 1, !dbg !38
  br label %20, !dbg !39

20:                                               ; preds = %11
  %21 = load i32, i32* %4, align 4, !dbg !40
  %22 = add nsw i32 %21, 1, !dbg !40
  store i32 %22, i32* %4, align 4, !dbg !40
  br label %7, !dbg !41, !llvm.loop !42

23:                                               ; preds = %7
  call void @llvm.dbg.declare(metadata i32* %5, metadata !44, metadata !DIExpression()), !dbg !46
  store i32 0, i32* %5, align 4, !dbg !46
  br label %24, !dbg !47

24:                                               ; preds = %45, %23
  %25 = load i32, i32* %5, align 4, !dbg !48
  %26 = load i32, i32* @MAX_SIZE, align 4, !dbg !50
  %27 = sub nsw i32 %26, 1, !dbg !51
  %28 = icmp slt i32 %25, %27, !dbg !52
  br i1 %28, label %29, label %48, !dbg !53

29:                                               ; preds = %24
  %30 = load i8*, i8** %3, align 8, !dbg !54
  %31 = load i32, i32* %5, align 4, !dbg !56
  %32 = add nsw i32 %31, 1, !dbg !57
  %33 = sext i32 %32 to i64, !dbg !54
  %34 = getelementptr inbounds i8, i8* %30, i64 %33, !dbg !54
  %35 = load i8, i8* %34, align 1, !dbg !54
  %36 = sext i8 %35 to i32, !dbg !54
  %37 = load i8*, i8** %3, align 8, !dbg !58
  %38 = load i32, i32* %5, align 4, !dbg !59
  %39 = sext i32 %38 to i64, !dbg !58
  %40 = getelementptr inbounds i8, i8* %37, i64 %39, !dbg !58
  %41 = load i8, i8* %40, align 1, !dbg !60
  %42 = sext i8 %41 to i32, !dbg !60
  %43 = xor i32 %42, %36, !dbg !60
  %44 = trunc i32 %43 to i8, !dbg !60
  store i8 %44, i8* %40, align 1, !dbg !60
  br label %45, !dbg !61

45:                                               ; preds = %29
  %46 = load i32, i32* %5, align 4, !dbg !62
  %47 = add nsw i32 %46, 1, !dbg !62
  store i32 %47, i32* %5, align 4, !dbg !62
  br label %24, !dbg !63, !llvm.loop !64

48:                                               ; preds = %24
  call void @llvm.dbg.declare(metadata i32* %6, metadata !66, metadata !DIExpression()), !dbg !68
  store i32 0, i32* %6, align 4, !dbg !68
  br label %49, !dbg !69

49:                                               ; preds = %68, %48
  %50 = load i32, i32* %6, align 4, !dbg !70
  %51 = load i32, i32* @MAX_SIZE, align 4, !dbg !72
  %52 = icmp slt i32 %50, %51, !dbg !73
  br i1 %52, label %53, label %71, !dbg !74

53:                                               ; preds = %49
  %54 = load i32, i32* %6, align 4, !dbg !75
  %55 = sext i32 %54 to i64, !dbg !78
  %56 = getelementptr inbounds [64 x i8], [64 x i8]* @check, i64 0, i64 %55, !dbg !78
  %57 = load i8, i8* %56, align 1, !dbg !78
  %58 = zext i8 %57 to i32, !dbg !78
  %59 = load i8*, i8** %3, align 8, !dbg !79
  %60 = load i32, i32* %6, align 4, !dbg !80
  %61 = sext i32 %60 to i64, !dbg !79
  %62 = getelementptr inbounds i8, i8* %59, i64 %61, !dbg !79
  %63 = load i8, i8* %62, align 1, !dbg !79
  %64 = zext i8 %63 to i32, !dbg !81
  %65 = icmp ne i32 %58, %64, !dbg !82
  br i1 %65, label %66, label %67, !dbg !83

66:                                               ; preds = %53
  store i32 0, i32* %2, align 4, !dbg !84
  br label %72, !dbg !84

67:                                               ; preds = %53
  br label %68, !dbg !86

68:                                               ; preds = %67
  %69 = load i32, i32* %6, align 4, !dbg !87
  %70 = add nsw i32 %69, 1, !dbg !87
  store i32 %70, i32* %6, align 4, !dbg !87
  br label %49, !dbg !88, !llvm.loop !89

71:                                               ; preds = %49
  store i32 1, i32* %2, align 4, !dbg !91
  br label %72, !dbg !91

72:                                               ; preds = %71, %66
  %73 = load i32, i32* %2, align 4, !dbg !92
  ret i32 %73, !dbg !92
}
