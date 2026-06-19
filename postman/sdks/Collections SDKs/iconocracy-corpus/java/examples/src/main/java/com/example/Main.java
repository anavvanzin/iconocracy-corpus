package com.example;

import com.iconocracycorpussdk.IconocracyCorpusSdk;
import com.iconocracycorpussdk.exceptions.ApiError;

public class Main {

  public static void main(String[] args) {
    IconocracyCorpusSdk iconocracyCorpusSdk = new IconocracyCorpusSdk();

    try {
      Object response = iconocracyCorpusSdk.get.getData();

      System.out.println(response);
    } catch (ApiError e) {
      e.printStackTrace();
    }

    System.exit(0);
  }
}
