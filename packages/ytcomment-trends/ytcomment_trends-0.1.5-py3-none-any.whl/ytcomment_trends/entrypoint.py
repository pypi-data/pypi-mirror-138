import argparse
import matplotlib.pyplot as plt
from .main import CommentAnalyzer

def entrypoint():
    """Entrypoint for the ytcomment_trends package
    """
    parser = argparse.ArgumentParser(prog='ytcomment_trends', usage='ytcomment_trends -v pR2E2OatMTQ -k hogefuga', description='ytcomment_trends: YouTube comment trends analysis tool using oseti')
    parser.add_argument('-v', '--video_id', help='YouTube video id', type=str, required=True)
    parser.add_argument('-k', '--key', help='YouTube API key', type=str, required=True)
    args = parser.parse_args()

    print(args.key)

    ca = CommentAnalyzer(args.video_id, args.key)
    ca_comments, _ = ca.get_comments()
    ca_analyzed = ca.get_analyzed_comments(ca_comments)
    ca_summarized = ca.get_summarized_comments(ca_analyzed)

    fig, ax1 = plt.subplots()
    t = ca_summarized.keys()

    color = 'tab:red'
    ax1.set_xlabel('datetime comment posted')
    ax1.set_ylabel('number of comments', color=color)
    ax1.plot(t, [v['comments'] for v in ca_summarized.values()], color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()

    oseti_scores = [v['oseti_score'] for v in ca_summarized.values()]

    color = 'tab:blue'
    ax2.set_ylabel('negative / positive', color=color)
    ax2.plot(t, oseti_scores, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    plt.ylim(-1.2, 1.2)
    plt.title("YouTube Video Comment Trends for " + args.video_id)
    plt.grid(True)

    fig.tight_layout()
    plt.show()

if __name__ == "__main__":
    entrypoint()