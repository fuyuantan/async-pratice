最近在看 LLM MCP，代码里面有异步编程，所以找了异步编程的东西看看。

掌握 Python 异步编程，了解何时使用 async、async with 和 await。

	• 使用 async
	1. 定义异步函数时：当你需要创建一个可以挂起执行并让出控制权的函数。
	async def my_function():
	    # 这是一个异步函数
	    pass
	2. 定义异步方法时：在类中定义异步方法。 
	class MyClass:
	    async def async_method(self):
	      # 这是一个异步方法
	       pass
	3. 定义异步生成器时：使用 async for 语句的生成器。
	async def async_generator():
	        for i in range(10):
	                await asyncio.sleep(0.1)
	                yield i
	 

	• 使用 async with
	1. 使用异步上下文管理器时：当你需要在异步函数中使用支持异步上下文管理协议的对象。 
	async def example():
	    async with aiohttp.ClientSession() as session:
	      # 在这个块中使用session
	    pass
	
	2. 需要自动化异步资源管理时：如异步文件操作、数据库连接等。 
	async def example():
	        async with AsyncDatabase() as db:
	                await db.execute("SELECT * FROM table")


	• 使用 await
	1. 调用异步函数时：当你需要等待一个协程（异步函数的结果）完成。 
	async def main():
	        result = await fetch_data()
	
	2. 等待异步操作完成时：如I/O操作、网络请求等。 
	async def get_page(url):
	        async with aiohttp.ClientSession() as session:
	                response = await session.get(url)
	                return await response.text()
	
	3. 等待异步任务或Future对象时： 
	task = asyncio.create_task(long_running_job())
	result = await task
	4. 等待其他可等待对象时：包括协程、任务和 Future。 
	await asyncio.sleep(1)  # 等待一个内置的异步函数
	

	• 记住的关键点
	1. async 修饰函数/方法定义，将其标记为协程函数。
	2. await 只能在 async 函数内部使用，用于等待协程、任务或 Future 完成。
	3. async with 用于异步上下文管理器，自动调用对象的__aenter__和__aexit__方法。
	4. 不能直接调用异步函数，必须使用 await 或将其包装成任务。
	5. 在异步函数中应该避免使用阻塞操作，应使用相应的异步版本。
![image](https://github.com/user-attachments/assets/84a6533e-e4b1-425e-9d9a-279e7bb68dc7)
