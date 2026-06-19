package com.iconocracycorpussdk.models;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.List;
import lombok.Builder;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.ToString;
import lombok.With;
import lombok.extern.jackson.Jacksonized;

@Data
@Builder
@With
@ToString
@EqualsAndHashCode
@Jacksonized
public class UpdateDiaryParameters {

  @JsonInclude(JsonInclude.Include.ALWAYS)
  @JsonProperty("Authorization")
  private String authorization;

  @JsonInclude(JsonInclude.Include.ALWAYS)
  private List<Object> requestBody;

  // Overwrite lombok builder methods
  public static class UpdateDiaryParametersBuilder {

    /**
     * Flag to track if the authorization property has been set.
     */
    private boolean authorization$set = false;

    /**
     * Flag to track if the requestBody property has been set.
     */
    private boolean requestBody$set = false;

    public UpdateDiaryParametersBuilder authorization(String authorization) {
      this.authorization$set = true;
      this.authorization = authorization;
      return this;
    }

    public UpdateDiaryParametersBuilder requestBody(List<Object> requestBody) {
      this.requestBody$set = true;
      this.requestBody = requestBody;
      return this;
    }

    public UpdateDiaryParameters build() {
      if (!authorization$set) {
        throw new IllegalStateException("authorization is required");
      }
      if (!requestBody$set) {
        throw new IllegalStateException("requestBody is required");
      }
      return new UpdateDiaryParameters(authorization, requestBody);
    }
  }
}
