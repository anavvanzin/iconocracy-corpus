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
public class PostDataRequest {

  @JsonProperty("name")
  private JsonNullable<String> name;

  @JsonIgnore
  public String getName() {
    return name.orElse(null);
  }

  // Overwrite lombok builder methods
  public static class PostDataRequestBuilder {

    private JsonNullable<String> name = JsonNullable.undefined();

    @JsonProperty("name")
    public PostDataRequestBuilder name(String value) {
      this.name = JsonNullable.of(value);
      return this;
    }
  }
}
