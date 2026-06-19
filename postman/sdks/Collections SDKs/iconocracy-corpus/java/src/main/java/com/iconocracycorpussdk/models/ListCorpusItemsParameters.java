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
public class ListCorpusItemsParameters {

  @JsonProperty("country")
  private JsonNullable<String> country;

  @JsonProperty("regime")
  private JsonNullable<String> regime;

  @JsonProperty("q")
  private JsonNullable<String> q;

  @JsonIgnore
  public String getCountry() {
    return country.orElse(null);
  }

  @JsonIgnore
  public String getRegime() {
    return regime.orElse(null);
  }

  @JsonIgnore
  public String getQ() {
    return q.orElse(null);
  }

  // Overwrite lombok builder methods
  public static class ListCorpusItemsParametersBuilder {

    private JsonNullable<String> country = JsonNullable.undefined();

    @JsonProperty("country")
    public ListCorpusItemsParametersBuilder country(String value) {
      this.country = JsonNullable.of(value);
      return this;
    }

    private JsonNullable<String> regime = JsonNullable.undefined();

    @JsonProperty("regime")
    public ListCorpusItemsParametersBuilder regime(String value) {
      this.regime = JsonNullable.of(value);
      return this;
    }

    private JsonNullable<String> q = JsonNullable.undefined();

    @JsonProperty("q")
    public ListCorpusItemsParametersBuilder q(String value) {
      this.q = JsonNullable.of(value);
      return this;
    }
  }
}
