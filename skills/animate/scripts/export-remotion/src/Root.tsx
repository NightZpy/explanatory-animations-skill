import React from "react";
import { Composition } from "remotion";
import { Lifecycle, lifecycleSchema, defaultLifecycle, lifecycleDuration } from "./compositions/Lifecycle";
import { TextScramble, scrambleSchema, defaultScramble, scrambleDuration } from "./compositions/TextScramble";

export const Root: React.FC = () => (
  <>
    <Composition
      id="Lifecycle"
      component={Lifecycle}
      durationInFrames={lifecycleDuration(defaultLifecycle, 60)}
      fps={60}
      width={1920}
      height={1080}
      defaultProps={defaultLifecycle}
      schema={lifecycleSchema}
      calculateMetadata={({ props, defaultProps }) => {
        const merged = { ...defaultProps, ...props };
        return {
          props: merged,
          durationInFrames: lifecycleDuration(merged, 60),
        };
      }}
    />

    <Composition
      id="LifecycleVertical"
      component={Lifecycle}
      durationInFrames={lifecycleDuration(defaultLifecycle, 60)}
      fps={60}
      width={1080}
      height={1920}
      defaultProps={{ ...defaultLifecycle, vertical: true }}
      schema={lifecycleSchema}
    />

    <Composition
      id="TextScramble"
      component={TextScramble}
      durationInFrames={scrambleDuration(defaultScramble, 60)}
      fps={60}
      width={1920}
      height={1080}
      defaultProps={defaultScramble}
      schema={scrambleSchema}
    />

    <Composition
      id="TextScrambleVertical"
      component={TextScramble}
      durationInFrames={scrambleDuration(defaultScramble, 60)}
      fps={60}
      width={1080}
      height={1920}
      defaultProps={defaultScramble}
      schema={scrambleSchema}
    />
  </>
);
