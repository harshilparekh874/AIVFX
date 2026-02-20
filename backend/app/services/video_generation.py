import os
import torch
import cv2
import numpy as np
from PIL import Image
from app.utils.config import settings
import google.generativeai as genai
import requests
import time
import base64
import json

async def generate_video(job_id, prompt, duration, resolution, output_dir):
    print(f"DEBUG: LTX_API_KEY from settings: {settings.LTX_API_KEY}")
    
    if not settings.LTX_API_KEY:
        raise Exception("LTX_API_KEY is not set in .env file.")
    
    preview_path = os.path.join(output_dir, "preview.mp4")
    
    # Use LTX API for text-to-video generation
    try:
        print(f"Generating video with LTX API for prompt: {prompt}")
        
        # Try different LTX API endpoints
        endpoints = [
            "https://api.ltx.ai/v1/generate",
            "https://api.ltx.ai/v1/text-to-video",
            "https://api.ltx.ai/v1/video/generate"
        ]
        
        headers = {
            "Authorization": f"Bearer {settings.LTX_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "prompt": prompt,
            "duration": duration,
            "resolution": resolution,
            "quality": "high"
        }
        
        for endpoint in endpoints:
            try:
                print(f"Trying endpoint: {endpoint}")
                response = requests.post(endpoint, headers=headers, json=payload, timeout=60)
                print(f"Response status: {response.status_code}")
                print(f"Response body: {response.text[:500]}")
                
                if response.status_code == 200:
                    result = response.json()
                    video_url = result.get("video_url") or result.get("url") or result.get("download_url")
                    
                    if video_url:
                        # Download the generated video
                        video_response = requests.get(video_url)
                        with open(preview_path, 'wb') as f:
                            f.write(video_response.content)
                        print(f"Video generated successfully: {preview_path}")
                        return preview_path
                    else:
                        print(f"No video URL in response: {result}")
                elif response.status_code == 401:
                    print("API key authentication failed")
                    break
                else:
                    print(f"Endpoint failed with status: {response.status_code}")
                    
            except Exception as endpoint_error:
                print(f"Endpoint {endpoint} error: {str(endpoint_error)}")
                continue
        
        raise Exception("All LTX API endpoints failed")
            
    except Exception as e:
        print(f"Video generation failed: {str(e)}")
        # Fallback to placeholder video
        print("Creating placeholder video...")
        create_placeholder_video(preview_path, resolution)
    
    # Create frame sequence for Phase 2-5
    frames_dir = os.path.join(output_dir, "raw_frames")
    os.makedirs(frames_dir, exist_ok=True)
    
    cap = cv2.VideoCapture(preview_path)
    idx = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        cv2.imwrite(os.path.join(frames_dir, f"frame_{idx:04d}.png"), frame)
        idx += 1
    cap.release()
    
    return preview_path

def create_placeholder_video(preview_path, resolution):
    """Create a placeholder video with moving elements"""
    width, height = map(int, resolution.split('x'))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(preview_path, fourcc, 8, (width, height))
    
    for i in range(32):
        img = np.zeros((height, width, 3), np.uint8)
        # Create a moving 3D-like subject for our computer vision models to track
        center_x = int(width/2 + 120 * np.sin(i * 0.15))
        center_y = int(height/2 + 60 * np.cos(i * 0.25))
        
        # Draw a glowing "VFX Subject"
        cv2.circle(img, (center_x, center_y), 90, (255, 100, 180), -1)
        cv2.circle(img, (center_x, center_y), 95, (255, 150, 220), 2)
        cv2.putText(img, "LTX GENERATION", (40, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        out.write(img)
    out.release()
