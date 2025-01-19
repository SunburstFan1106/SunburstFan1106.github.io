import subprocess
import os

def git_sync(commit_message):
    """
    执行git add、commit和push操作
    """
    try:
        # 确保在正确的目录
        root_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(root_dir)
        
        # Git add
        subprocess.run(['git', 'add', '.'], check=True)
        
        # Git commit
        subprocess.run(['git', 'commit', '-m', commit_message], check=True)
        
        # Git push
        subprocess.run(['git', 'push'], check=True)
        
        print("Git同步完成！")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Git操作失败: {str(e)}")
        return False
    except Exception as e:
        print(f"发生错误: {str(e)}")
        return False