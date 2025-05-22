---
type: post
title: 现代C语言：C23标准中值得注意的变化
date: 2023-09-14 0:00
updated: 2023-09-14 0:00
categories: 开发与代码
tags:
  - C
  - 现代编程语言
---

虽然没有固定标准，但一般将C99之后的C语言标准称为“现代C语言”；目前的最新标准为C23；

## C23标准中值得注意的变化

以下是一部分我认为比较重要的变化，完整变化列表可以参阅 <https://en.cppreference.com/w/c/23> 或ISO标准文档。

## 替代

- `<assert.h>`中的`static_assert()`宏被替代，变成了`static_assert`关键字；
- `<threads.h>`中的`thread_local()`宏被替代，变成了`thread_local`关键字；
- `<time.h>`中的`ctime()`函数弃用，请使用`ctime_s()`替代；
- `<time.h>`中的`asctime()`函数弃用，请使用`asctime_s()`替代；
- `<stdnoreturn.h>`与`_Noreturn`标识符均弃用；
- `<stdalign.h>`中的`alignas()`和`alignof()`宏被弃用，请直接使用`_Alignas`和`_Alignof`关键字；

<!--more-->

## 新增

- C23新增了三个十进制浮点数数据类型（关键字）：`_Decimal32`、`_Decimal64`和`_Decimal128`，对应的后缀是`DF`、`DD`和`DL`。它们的最大值分别如下：

```
DEC32_MAX 9.999999E96DF
DEC64_MAX 9.999999999999999E384DD
DEC128_MAX 9.999999999999999999999999999999999E6144DL
```

- C23可以使用二进制字面量了，使用`0b`或者`0B`开头，例如：

```c
int num = 0b1011;
```

- C23的字面量可以加分隔符了，增强可读性，例如：

```c
int num2 = 100'020'050;
```

- C23添加了`bool`、`true`、`false`三个关键字，可以像C++一样定义布尔类型了：

```c
bool choice = true;
```

- C23新加了`nullptr`关键字，它是`nullptr_t`类型的，可以被强制转换为任意指针类型（传统空指针）及布尔类型（可用于逻辑判断）：

```c
void func(int a, nullptr_t b) {
	//...
}

func(10, nullptr);

int *a = nullptr;

if(!a) {
    printf("A is nullptr");
}
```

- C23添加了双括号属性（Attributes）了，常用的比如：
  - `[[deprecated]]`
  - `[[nodiscard]]`
  - `[[noreturn]]`
  - `[[maybe_unused]]`
- C23新加了一些预编译命令，常用的比如：
  - `#elifdef`
  - `#elifndef`
  - `#warning`：让编译器抛出警告
  - `#embed`：让编译器直接内嵌二进制数据

```c
static const char song[] = {
    #embed <music.wav>
};
```
- C23增加了空初始化列表支持，也就是说：

```c
int a[5] = { 0 };
// 可以直接写成
int a[5] = {};
// 等价于
int a[5] = { 0, 0, 0, 0, 0 };
```

- C23的宏支持`__VA_OPT__`了，能更方便地解决使用宏时末尾符号的问题；
- C23给`<stdio.h>`中的`printf()`函数添加了`%b`和`%B`支持，能像打印16进制（`%x %X`）一样直接打印二进制数据了；`scanf()`也增加了`%b`支持；
- C23给`<string.h>`增加了`memccpy()`，与`memcpy()`类似但遇到某个特定值时会立刻停止复制；
- C23给`<string.h>`增加了`strdup()`与`strndup()`，用于复制出一个新的（部分）字符串；
- C23引入了函数定义时的匿名参数，如果一个参数因为某种原因必须被传递但却不被使用，就可以把它设置为匿名参数：

```c
int func(int num, char*)
{
	return num1 + 5;
}
```

- C23引入了`constexpr`支持，可以定义编译期**变量**了；

```c
constexpr int c = 10/2;
```

- C23将`auto`关键字的语义进行了修改。`auto`原本作为Storage class specifier时极少使用，因此`auto`在C23里变为了**自动类型推导关键字**。是的，C语言也可以使用auto推导了：

```c
const char* func()
{
	return "Hello!";
}

auto fRet = func();
```

- C23增加了对“X位整数”的支持，类型关键字为`_BitInt()`，编程时可以自由指定整数是几位。类型对应的字面量后缀是`wb/WB`和`uwb/UWB`例如：

```c
// 12位无符号整数
unsigned _BitInt(12) a = 0uwb;
```

- `<uchar.h>`中加入类型`char8_t`，存储UTF-8字符。类型对应的字面量前缀是`u8`。例如：

```c
char8_t srt[] = u8"你好！";
```

- C23允许给enum（枚举类型）指定类型了，如果不指定类型则默认为int。例如：

```c
enum flags: unsigned long {
    err1 = 0xCOOOFFFF;
    err2 = 0xC0010000;
}
```

- C23引入了typeof支持：

```c
int a = 10;
typeof(a) b = 5;
```

- `<stdarg.h>`中用于实现可变函数参数的宏 `va_start`不再强制需要第二个参数，拥有可变参数的函数也不再需要至少一个有名参数了：

```c
int add_nums_C23(...)  //不需要有名参数
{
    int result = 0;
    va_list args;
    va_start(args); //不需要第二个参数
 
    int count = va_arg(args, int);
    for (int i = 0; i < count; ++i) {
        result += va_arg(args, int);
    }
 
    va_end(args);
    return result;
}
```

## 删除

- `<stdlib.h>`中的`realloc()`不再支持size为0的情况，改为未定义行为；
- C23取消了对三字母词（Trigraph）的支持。三字母词是一种转义字符，由`??`开头。例如在字面量中使用`??)`代替`]`。
  - 参考：<https://blog.csdn.net/daheiantian/article/details/6095507>
- C23规定整数必须使用补码存储，不应再使用原码和反码；
- C23决定不再支持K&R格式。K&R格式是一种老式C语言写法，例如：

```c
// K&R
func1();

func1(a, b, c)
    int a;
    char* b;
    int c;
{
    d = a + c;
    return d;
}

// 等价于现代语法
int func1(int a, char* b, int c);

int func1(int a, char* b, int c)
{
    int d = a + c;
    return d;
}
```