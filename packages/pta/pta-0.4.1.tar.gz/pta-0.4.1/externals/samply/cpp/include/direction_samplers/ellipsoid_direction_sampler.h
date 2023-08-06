// Copyright (c) 2021 ETH Zurich, Mattia Gollub (mattia.gollub@bsse.ethz.ch)
// Computational Systems Biology group, D-BSSE
//
// This software is freely available under the GNU General Public License v3.
// See the LICENSE file or http://www.gnu.org/licenses/ for further information.

#ifndef SAMPLY_ELLIPSOID_DIRECTION_SAMPLER_H
#define SAMPLY_ELLIPSOID_DIRECTION_SAMPLER_H

#include <Eigen/Dense>

#include "commons.h"
#include "helpers/sampling_helper.h"
#include "rays_packet.h"
#include "reparametrized_object.h"

namespace samply {

/**
 * @brief Samples directions from an n-dimensional ellipsoid.
 *
 * @tparam Scalar Type used to describe the directions.
 */
template <typename ScalarType> class EllipsoidDirectionSampler {
  public:
    /**
     * @brief Type used to describe the directions.
     */
    typedef ScalarType Scalar;

    /**
     * @brief Type of rays packets constructed from this sampler.
     */
    typedef RaysPacket<ScalarType> RaysPacketType;

    EllipsoidDirectionSampler(const AffineTransform<Scalar>& directions_transform)
        : directions_transform_(directions_transform)
        , dimensionality_(directions_transform.get_linear().cols())
    {}

    Matrix<Scalar> get_directions(const Eigen::Index num_directions);

    /**
     * @brief Get the dimensionality of the sampled directions.
     *
     * @return The dimensionality of the sampled directions.
     */
    Eigen::Index dimensionality() const { return dimensionality_; }

    ReparametrizedObject<EllipsoidDirectionSampler<Scalar>>
    get_optimally_reparametrized_descriptor() const;

  private:
    const AffineTransform<Scalar> directions_transform_;
    const Eigen::Index dimensionality_;

    // Helper object used to generate random numbers.
    SamplingHelper sampling_helper_;
};

//==============================================================================
//	EllipsoidDirectionSampler public methods implementation.
//==============================================================================

template <typename ScalarType>
Matrix<ScalarType>
EllipsoidDirectionSampler<ScalarType>::get_directions(const Eigen::Index num_directions)
{
    return directions_transform_ *
           sampling_helper_.get_random_directions<Scalar>(
               static_cast<int>(dimensionality()), static_cast<int>(num_directions));
}

template <typename ScalarType>
ReparametrizedObject<EllipsoidDirectionSampler<ScalarType>>
EllipsoidDirectionSampler<ScalarType>::get_optimally_reparametrized_descriptor() const
{
    return ReparametrizedObject<EllipsoidDirectionSampler<Scalar>>(
        EllipsoidDirectionSampler<Scalar>(
            AffineTransform<double>::identity(dimensionality())),
        directions_transform_, directions_transform_.inverse());
}

} // namespace samply

#endif