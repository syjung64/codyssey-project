import requests
from bs4 import BeautifulSoup
import json
import time

def install_beautifulsoup():
    """BeautifulSoup 설치 확인 및 설치"""
    try:
        import bs4
        print("BeautifulSoup이 이미 설치되어 있습니다.")
        return True
    except ImportError:
        print("BeautifulSoup을 설치합니다...")
        import subprocess
        subprocess.check_call(["pip", "install", "beautifulsoup4"])
        print("BeautifulSoup 설치가 완료되었습니다.")
        return True

def get_kbs_news_headlines():
    """KBS 뉴스 헤드라인을 가져오는 함수"""
    print("KBS 뉴스 크롤링을 시작합니다...")
    
    # BeautifulSoup 설치 확인
    install_beautifulsoup()
    
    # User-Agent 헤더 설정 (봇 차단 방지)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    headlines = []
    try:     
        # KBS 뉴스 웹페이지 URL들
        web_urls = [
            'https://news.kbs.co.kr/news/pc/main/main.html',
            'https://news.kbs.co.kr'
        ]
        
        for url in web_urls:
            try:
                print(f"웹페이지 접근 시도: {url}")
                response = requests.get(url, headers=headers, timeout=15)
                
                if response.status_code == 200:
                    print(f"웹페이지 연결 성공: {url}")
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # 다양한 CSS 선택자로 헤드라인 찾기
                    selectors = [
                        #'h2 a', 'h3 a', 'h4 a',  # 제목 태그
                        #'.title a', '.tit a', '.headline a',  # 클래스 기반
                        'a[href*="/news/view"]', 'a[href*="/news/pc/view"]',  # 뉴스 링크
                        #'.news-list a', '.list-news a',  # 뉴스 리스트
                        #'article a', '.article a',  # 아티클
                        #'a[href*="news"]'  # 뉴스 관련 링크
                    ]
                    
                    for selector in selectors:
                        elements = soup.select(selector)
                        for element in elements:
                            text = element.get_text().strip()
                            if text and len(text) > 5 and text not in headlines:
                                headlines.append(text)
                        
                        if headlines:
                            print(f"선택자 '{selector}'로 {len(headlines)}개의 헤드라인을 찾았습니다.")
                        
            except Exception as e:
                print(f"웹페이지 접근 오류 ({url}): {e}")
                continue
        
        # 여전히 헤드라인을 찾지 못한 경우 대안 제공
        if not headlines:
            print("KBS 뉴스 사이트의 구조가 변경되었거나 접근이 제한되었습니다.")
            
            # 샘플 헤드라인 제공 (실제 크롤링이 실패한 경우)
            headlines = [
                "KBS 뉴스 크롤링 실패 - 사이트 구조 변경 또는 접근 제한",
            ]
            print("샘플 헤드라인을 제공합니다.")
    
    except Exception as e:
        print(f"크롤링 중 오류 발생: {e}")
        headlines = ["크롤링 오류 발생"]
    
    return headlines

def main():
    """메인 함수"""
    try:
        # KBS 뉴스 헤드라인 가져오기
        headlines = get_kbs_news_headlines()
        
        # 결과 출력
        print(f"\n=== KBS 뉴스 헤드라인 ({len(headlines)}개) ===")
        for i, headline in enumerate(headlines, 1):
            print(f"{i}. {headline}")
        
        # List 객체로 저장 (요구사항에 따라)
        headlines_list = headlines
        print(f"\nList 객체에 {len(headlines_list)}개의 헤드라인이 저장되었습니다.")
        
        return headlines_list
        
    except Exception as e:
        print(f"프로그램 실행 중 오류: {e}")
        return []

if __name__ == "__main__":
    main()
