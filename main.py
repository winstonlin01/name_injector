from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api import logger, AstrBotConfig
from astrbot.api.star import Context, Star, register, StarTools
from astrbot.api.provider import LLMResponse, ProviderRequest


@register("name_injector", "winstonlin01", "name_injector", "1.0.0")
class name_injector(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""

    # 注册指令的装饰器。指令名为 helloworld。注册成功后，发送 `/helloworld` 就会触发这个指令，并回复 `你好, {user_name}!`
    @filter.on_llm_request()
    async def add_context_prompt(self, event: AstrMessageEvent, req: ProviderRequest):
        """
        在 LLM 请求发起前，将当前发送者的用户名植入 System Prompt
        """
        # 1. 获取发送者姓名
        user_name = event.get_sender_name()
        
        # 2. 构造注入文本 (根据需要调整格式，例如 "当前对话用户是：xxx")
        user_context = f"\n[User Context: Current user is {user_name}]"
        
        # 3. 追加到系统提示词
        if req.system_prompt:
            req.system_prompt += user_context
        else:
            req.system_prompt = user_context
        req.extra_user_content_parts.append(user_name)
        # 日志打印（可选，用于调试确认）
        logger.debug(f"已为用户 {user_name} 注入上下文")

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
