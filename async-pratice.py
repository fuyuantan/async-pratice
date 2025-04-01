# 1. 基础异步函数示例
import asyncio


async def hello_world():
    print("开始执行")
    await asyncio.sleep(1)  # 模拟I/O操作
    print("Hello, World!")
    return "完成"


async def main_basic():
    result = await hello_world()
    print(f"结果: {result}")


# 运行基础示例
asyncio.run(main_basic())


# 2. 多任务并发
async def task_1():
    await asyncio.sleep(2)
    return "任务1完成"


async def task_2():
    await asyncio.sleep(1)
    return "任务2完成"


async def main_concurrent():
    # 创建任务
    task_obj_1 = asyncio.create_task(task_1())
    task_obj_2 = asyncio.create_task(task_2())

    # 等待所有任务完成
    results = await asyncio.gather(task_obj_1, task_obj_2)
    print(f"并发结果: {results}")


# 运行并发示例
asyncio.run(main_concurrent())

# 3. 使用aiohttp进行异步HTTP请求
import aiohttp


async def fetch_url(session, url):
    async with session.get(url) as response:
        return await response.text()


async def main_http():
    urls = [
        'https://httpbin.org/delay/1',
        'https://httpbin.org/delay/2',
        'https://httpbin.org/delay/3'
    ]

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        results = await asyncio.gather(*tasks)

        for i, result in enumerate(results):
            print(f"URL {i + 1} 响应长度: {len(result)}")


# 运行HTTP请求示例
asyncio.run(main_http())


# 4. 超时处理
async def slow_operation():
    await asyncio.sleep(5)
    return "这个操作太慢了"


async def main_timeout():
    try:
        # 设置2秒超时
        result = await asyncio.wait_for(slow_operation(), timeout=2)
        print(result)
    except asyncio.TimeoutError:
        print("操作超时！")


# 运行超时示例
asyncio.run(main_timeout())


# 5. 结合asyncio和aiohttp实现一个简单的爬虫
async def fetch_and_process(session, url):
    try:
        async with session.get(url, timeout=10) as response:
            if response.status == 200:
                data = await response.text()
                return f"URL: {url}, 状态: {response.status}, 数据长度: {len(data)}"
            return f"URL: {url}, 状态: {response.status}"
    except Exception as e:
        return f"URL: {url}, 错误: {str(e)}"


async def crawl_websites():
    websites = [
        "https://www.python.org",
        "https://docs.python.org/3/library/asyncio.html",
        "https://github.com",
        "https://httpbin.org/delay/4"
    ]

    # 使用aiohttp的ClientSession
    async with aiohttp.ClientSession() as session:
        # 为每个网站创建一个任务
        tasks = [fetch_and_process(session, site) for site in websites]

        # 设置总体超时为15秒
        try:
            results = await asyncio.wait_for(asyncio.gather(*tasks), timeout=15)
            for result in results:
                print(result)
        except asyncio.TimeoutError:
            print("整体操作超时！")


# 运行爬虫示例
asyncio.run(crawl_websites())


# 6. 使用asyncio.Queue实现生产者-消费者模式
async def producer(queue, n):
    for i in range(n):
        # 生产数据
        await queue.put(f"Item-{i}")
        print(f"生产者: 生产了 Item-{i}")
        await asyncio.sleep(0.5)

    # 表示生产结束
    await queue.put(None)


async def consumer(queue, id):
    while True:
        # 消费数据
        item = await queue.get()
        if item is None:
            # 收到结束信号
            print(f"消费者-{id}: 收到结束信号")
            queue.task_done()
            break

        print(f"消费者-{id}: 处理了 {item}")
        await asyncio.sleep(1)  # 模拟处理时间
        queue.task_done()


async def main_queue():
    # 创建队列
    queue = asyncio.Queue()

    # 创建一个生产者和两个消费者
    prod = asyncio.create_task(producer(queue, 5))
    cons1 = asyncio.create_task(consumer(queue, 1))
    cons2 = asyncio.create_task(consumer(queue, 2))

    # 等待所有任务完成
    await prod
    await queue.join()  # 等待队列处理完所有任务

    # 取消消费者任务
    cons1.cancel()
    cons2.cancel()

    print("所有任务完成！")


# 运行队列示例
asyncio.run(main_queue())


# 7. 异步上下文管理器
class AsyncTimer:
    def __init__(self, name):
        self.name = name

    async def __aenter__(self):
        self.start = asyncio.get_event_loop().time()
        print(f"开始计时: {self.name}")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        end = asyncio.get_event_loop().time()
        print(f"结束计时: {self.name}, 用时: {end - self.start:.2f}秒")


async def main_context():
    async with AsyncTimer("测试任务"):
        await asyncio.sleep(2)
        print("任务执行中...")


# 运行上下文管理器示例
asyncio.run(main_context())


# 8. 实现MCP相关的异步处理示例
class ModelSession:
    def __init__(self, model_name):
        self.model_name = model_name
        print(f"初始化模型会话: {model_name}")

    async def process_context(self, context):
        print(f"处理上下文: {context[:50]}...")
        await asyncio.sleep(1)  # 模拟模型处理时间
        return f"模型{self.model_name}的结果: 已处理{len(context)}字符"

    async def close(self):
        print(f"关闭模型会话: {self.model_name}")
        await asyncio.sleep(0.5)  # 模拟清理资源


async def model_context_protocol_demo():
    # 模拟MCP工作流程
    contexts = [
        "这是第一段上下文，包含了用户的查询和一些背景信息...",
        "这是第二段上下文，包含了更多的相关信息和历史交互...",
        "这是第三段上下文，包含了一些补充材料和要求..."
    ]

    # 异步创建会话
    session = ModelSession("GPT-5")

    try:
        # 并行处理多个上下文
        tasks = [session.process_context(ctx) for ctx in contexts]
        results = await asyncio.gather(*tasks)

        for i, result in enumerate(results):
            print(f"结果 {i + 1}: {result}")

    finally:
        # 确保会话被正确关闭
        await session.close()


# 运行MCP示例
asyncio.run(model_context_protocol_demo())