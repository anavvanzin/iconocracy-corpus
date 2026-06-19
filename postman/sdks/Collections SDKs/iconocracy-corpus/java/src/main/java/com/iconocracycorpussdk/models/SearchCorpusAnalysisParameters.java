package com.iconocracycorpussdk.models;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Builder;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.ToString;
import lombok.With;
import lombok.extern.jackson.Jacksonized;
import org.openapitools.jackson.nullable.JsonNullable;

@Data
@Builder
@With
@ToString
@EqualsAndHashCode
@Jacksonized
public class SearchCorpusAnalysisParameters {

  @JsonProperty("attr")
  private JsonNullable<String> attr;

  @JsonProperty("figure")
  private JsonNullable<String> figure;

  @JsonIgnore
  public String getAttr() {
    return attr.orElse(null);
  }

  @JsonIgnore
  public String getFigure() {
    return figure.orElse(null);
  }

  // Overwrite lombok builder methods
  public static class SearchCorpusAnalysisParametersBuilder {

    private JsonNullable<String> attr = JsonNullable.undefined();

    @JsonProperty("attr")
    public SearchCorpusAnalysisParametersBuilder attr(String value) {
      this.attr = JsonNullable.of(value);
      return this;
    }

    private JsonNullable<String> figure = JsonNullable.undefined();

    @JsonProperty("figure")
    public SearchCorpusAnalysisParametersBuilder figure(String value) {
      this.figure = JsonNullable.of(value);
      return this;
    }
  }
}
