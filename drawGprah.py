from PIL import Image as PILImage
import io


def draw_graph(graph):
    try:
        # 假设 graph.get_graph().draw_mermaid_png() 返回的是图像的二进制数据
        image_data = graph.get_graph().draw_mermaid_png()
        
        # 使用 PILImage 打开图像
        image = PILImage.open(io.BytesIO(image_data))
        
        # 显示图像（在支持图形界面的环境中）
        image.show()
        
    except Exception as e:
        print(f"An error occurred: {e}")
        # 这里可以处理异常或记录错误
